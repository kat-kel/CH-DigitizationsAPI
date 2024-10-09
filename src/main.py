import click
import casanova
import json
from rich.progress import Progress, BarColumn, MofNCompleteColumn, TimeElapsedColumn

from api_gallica import Gallica
from api_irht import IRHT


@click.command
@click.option("-i", "--infile", required=True)
@click.option("-c", "--column", required=True)
@click.option("-o", "--outfile", required=True)
def main(infile, column, outfile):
    results = {}
    infile_length = casanova.count(infile)
    with open(infile, mode="r", encoding="utf-8") as f, Progress(
        BarColumn(), MofNCompleteColumn(), TimeElapsedColumn()
    ) as p:
        t = p.add_task("", total=infile_length)
        reader = casanova.reader(f)
        for url in reader.cells(column):
            tld = Gallica.get_tld(url=url)
            if not results.get(tld):
                results.update({tld: {}})

            result = None
            results[tld].update({url: {}})

            if Gallica.is_url(url=url):
                ark = Gallica.get_ark(url=url)
                obj = Gallica.object(ark=ark)
                result = obj.model_dump()
                results[tld].update({url: result})

            elif IRHT.is_url(url=url):
                ark = IRHT.get_ark(url=url)
                obj = IRHT.object(ark=ark)
                result = obj.model_dump()
                results[tld].update({url: result})

            p.advance(t)

    with open(outfile, mode="w") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
