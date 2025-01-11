from constituency_data_extraction import process_line, map_abbreviated_to_full


def test_process_line() -> None:
    unprocessed_lines = [
        "Aberavon Lab Con 10,490 33.2% Stephen Kinnock No",
        "Thirsk and Malton Con Lab 25,154 44.5% Kevin Hollinrake No",
        "Wellingborough Con Lab 18,540 35.7% Peter Bone No",
        "Aberdeen South SNP Con 3,990 8.7% Stephen Flynn Yes"
    ]
    processed_lines = [
        ['Aberavon', 'Lab', 'Con', '10,490', '33.2%', 'Stephen Kinnock', 'No'],
        ['Thirsk and Malton', 'Con', 'Lab', '25,154', '44.5%', 'Kevin Hollinrake', 'No'],
        ['Wellingborough', 'Con', 'Lab', '18,540', '35.7%', 'Peter Bone', 'No'],
        ['Aberdeen South', 'SNP', 'Con', '3,990', '8.7%', 'Stephen Flynn', 'Yes']
    ]
    for i in range(0,3):
        assert process_line(unprocessed_lines[i]) == processed_lines[i]


def test_map_abbreviated_to_full() -> None:
    assert map_abbreviated_to_full('Con') == 'Conservatives'