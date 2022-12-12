import pytest

from .utils import get_mocked_file_content, get_mocked_filename


@pytest.fixture(params=[1, 2, 5, 10, 20])
def urls(request):
    url_list = [
        "https://en.wikipedia.org/wiki/Georgia_State_Route_74",
        "https://en.wikipedia.org/wiki/Mediated_reference_theory",
        "https://en.wikipedia.org/wiki/Thomas_Cromwell_Corner",
        "https://en.wikipedia.org/wiki/Livingston_Municipal_Airport_(Tennessee)",
        "https://en.wikipedia.org/wiki/Get_Physical_Music",
        "https://en.wikipedia.org/wiki/Photinia_lasiogyna",
        "https://en.wikipedia.org/wiki/2006_Top_League_Challenge_Series",
        "https://en.wikipedia.org/wiki/Stuart_Lester",
        "https://en.wikipedia.org/wiki/Jeremy_Bates_(tennis)",
        "https://en.wikipedia.org/wiki/Ai_Yanhan",
        "https://en.wikipedia.org/wiki/Motivator_(horse)",
        "https://en.wikipedia.org/wiki/Q-analog",
        "https://en.wikipedia.org/wiki/Yazan,_Mazandaran",
        "https://en.wikipedia.org/wiki/Rebecca_W._Keller",
        "https://en.wikipedia.org/wiki/UPI_College_Football_Player_of_the_Year",
        "https://en.wikipedia.org/wiki/I%27ll_Cry_Tomorrow_(book)",
        "https://en.wikipedia.org/wiki/Symmetry_of_second_derivatives",
        "https://en.wikipedia.org/wiki/Faustino_Garc%C3%ADa-Monc%C3%B3",
        "https://en.wikipedia.org/wiki/Kennedy_Avenue",
        "https://en.wikipedia.org/wiki/Shaina_Amin",
    ]
    n_urls = request.param
    yield url_list[:n_urls]


@pytest.fixture
def expected_filenames(urls):
    yield map(get_mocked_filename, urls)


@pytest.fixture
def expected_contents(urls):
    yield map(get_mocked_file_content, urls)
