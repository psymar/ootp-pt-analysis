from card_parsing.read_cards import parse_cards
from output_utils.generate_worksheet import generate_worksheet
from output_utils.worksheet_headers import batter_headers, pitcher_headers, data_headers, batter_freeze_col, pitcher_freeze_col, data_freeze_col, data_hidden_columns, batter_hidden_columns, pitcher_hidden_columns

import xlsxwriter

cards = parse_cards()

pitcher_cards = []
batter_cards = []

for card in cards:
    # All pitchers and batters who have stuff ratings higher than 30
    if card["position"] == "SP" or card["position"] == "RP" or card["position"] == "CL" or card["stu"] > 30:
        pitcher_cards.append(card)
    # All batters and pitchers who have overall contact higher than 40
    if ((card["position"] != "SP" and card["position"] != "RP" and card["position"] != "CL") or card["con"] > 40) and "-rp" not in str(card["t_CID"]) and "-sp" not in str(card["t_CID"]):
        batter_cards.append(card)

# Perform analysis here.

# Create sheet
workbook = xlsxwriter.Workbook('output/PTSheet.xlsx')
batter_sheet = workbook.add_worksheet("List-BAT")
pitcher_sheet = workbook.add_worksheet("List-PIT")
full_sheet = workbook.add_worksheet("Cards")

# Write different stats to sheet
generate_worksheet(batter_cards, batter_sheet, batter_headers, batter_freeze_col, batter_hidden_columns)
generate_worksheet(pitcher_cards, pitcher_sheet, pitcher_headers, pitcher_freeze_col, pitcher_hidden_columns)
generate_worksheet(cards, full_sheet, data_headers, data_freeze_col, data_hidden_columns)

workbook.close()