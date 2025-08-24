import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import click
import pendulum
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from clubs import CLUBS


def get_latest_manifest():
    latest = max(os.listdir("clubs/manifests"))
    with open(f"clubs/manifests/{latest}") as f_:
        return json.load(f_)

@click.command()
@click.option("--manifest-dir")
@click.option("--overwrite", is_flag=True, default=False)
@click.option("--all-ids",  is_flag=True, default=False)
@click.option("--base-url", default="https://www.golf.co.nz/club-detail?clubid={club_id}")
def main(
    manifest_dir,
    overwrite,
    all_ids,
    base_url,
):
    epoch: int = pendulum.now().int_timestamp

    driver = webdriver.Chrome()

    clubs = {str(k): v for k, v in CLUBS.items()}

    for club_id, club_info in clubs.items():
        if club_info == {}:
            continue

        driver.get(base_url.format(club_id=club_id))

        properties = {
            "name": '//*[@id="ctl55"]/div[1]/div/div/div/div/h1/span/span',
            "description": '//*[@id="ctl55"]/section/div[1]/div/div[1]/div/div',
            "phone": '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[2]/div/div[1]/div/p/span',
            "email": '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[2]/div/div[1]/div/p/a[1]',
            "address1": '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[1]/div/p[1]/span[1]',
            "address2": '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[1]/div/p[1]/span[2]',
            "address3": '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[1]/div/p[1]/span[3]',
            "postcode": '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[1]/div/p[1]/span[4]',
            "total_men": '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[2]/div/div[2]/div/p/span[4]',
            "total_women": '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[2]/div/div[2]/div/p/span[5]',
        }

        print(f"Fetching club {club_id}")
        for property_name, property_xpath in properties.items():
            retries = 0

            element = None
            while retries < 3:
                try:
                    element = driver.find_element(By.XPATH, property_xpath)
                except NoSuchElementException:
                    retries += 1

                if element is not None:
                    break

            if element is None:
                clubs[club_id][property_name] = None
            else:
                clubs[club_id][property_name] = element.text

    with open(f"clubs/manifests/manifest_{epoch}.json", "w") as f:
        f.write(json.dumps(clubs, indent=2))


if __name__ == "__main__":
    main()
