from typing import Optional
import os
import argparse
import asyncio
import aiohttp
import aiofiles

from logger import init_logger


logger = init_logger("logging_conf.yaml", "fetcher")


MAX_TASK_QUEUE_SIZE = 1000
STOP_TASK = "STOP_TASK"
RESPONSE_OK = 200


async def fetch_url(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    if not isinstance(session, aiohttp.ClientSession):
        raise TypeError(
            f"Wrong type of 'session' argument. "
            f"Expected aiohttp.ClientSession, got {type(session)} instead."
        )

    async with session.get(url, ssl=False) as response:
        if response.status == RESPONSE_OK:
            return await response.text()


async def save_html(url: str, html: str, output_dir_name: str) -> None:
    output_filename = url.split("/")[-1]
    full_path = os.path.join(output_dir_name, output_filename)
    async with aiofiles.open(full_path, "w") as f:
        await f.write(html)


async def coro_fetcher(task_queue: asyncio.Queue, output_dir_name: str) -> None:
    async with aiohttp.ClientSession() as session:
        while True:
            url = await task_queue.get()
            if url == STOP_TASK:
                await task_queue.put(STOP_TASK)
                task_queue.task_done()
                return

            try:
                html = await fetch_url(session, url)
                if html:
                    await save_html(url, html, output_dir_name)
                    logger.info("Task done: %s", url)
                else:
                    logger.warning("Bad response: %s", url)
            except Exception as e:
                logger.error(
                    'Unexpected error occurred while processing url. '
                    'URL: %s; Exception: %s',
                    url,
                    str(e)
                )
            finally:
                task_queue.task_done()


def get_parser():
    parser = argparse.ArgumentParser(
        description="Loads urls listed in the input file and "
        "saves results to the output directory."
    )
    parser.add_argument(
        "-c",
        action="store",
        dest="n_simultaneous_requests",
        type=int,
        required=True,
        help="Number of simultaneous corutines.",
    )
    parser.add_argument(
        "-i",
        action="store",
        dest="input_filename",
        required=True,
        help="File with urls.",
    )
    parser.add_argument(
        "-o",
        action="store",
        dest="output_dir_name",
        required=True,
        help="Path to the directory for storing loaded files.",
    )
    return parser


async def coro_reader(task_queue: asyncio.Queue, input_filename: str):
    try:
        async with aiofiles.open(input_filename, "r") as f:
            async for line in f:
                await task_queue.put(line.strip())
    except Exception as e:
        logger.error("Unexpected error occurred during reading file: %s", str(e))
    finally:
        await task_queue.put(STOP_TASK)


async def main(args):
    logger.info("Start async url fetcher.")
    task_queue = asyncio.Queue(maxsize=MAX_TASK_QUEUE_SIZE)

    workers = [
        asyncio.create_task(coro_fetcher(task_queue, args.output_dir_name))
        for _ in range(args.n_simultaneous_requests)
    ]
    workers.append(
        asyncio.create_task(coro_reader(task_queue, args.input_filename))
    )

    await asyncio.gather(*workers)


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    asyncio.run(main(args))
