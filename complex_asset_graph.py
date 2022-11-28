import urllib.request
import zipfile
from cereal import *


# downloads the zip file as asset
@asset
def cereal_ratings_zip() -> None:
    urllib.request.urlretrieve(
        "https://dagster-git-tutorial-nothing-elementl.vercel.app/assets/cereal-ratings.csv.zip",
        "cereal-ratings.csv.zip",
    )


# unzips the zip file as asset
@asset(non_argument_deps={"cereal_ratings_zip"})
def cereal_ratings_csv() -> None:
    with zipfile.ZipFile("cereal-ratings.csv.zip", "r") as zip_ref:
        zip_ref.extractall(".")


@asset(non_argument_deps={"cereal_ratings_csv"})
def nabisco_cereal_ratings(nabisco_cereals):
    with open("cereal-ratings.csv", "r") as f:
        cereal_ratings = {
            row["name"]: row["rating"] for row in csv.DictReader(f.readlines())
        }

    result = {}
    for nabisco_cereal in nabisco_cereals:
        name = nabisco_cereal["name"]
        result[name] = cereal_ratings[name]

    return result