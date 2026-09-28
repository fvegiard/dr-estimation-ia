# NECA 2021-2022 parse report (layer: auto)

- Source: `/home/claude/data/livres/Neca 2022 OCR.pdf` (sha256 `ccb048510a949d329c789c4ede79fb049d6663658c6d20d36a0162c7711cc06e`), 531 PDF pages
- Output: `neca-2022.csv`, **14556 rows**, 14555 with all three labor units, 1 with a unit but no number printed
- Pages with a table header: 335; pages read from the OCR layer only: 3 [1, 56, 398]
- Units: E=10800, C=2163, M=1483, LF=72, FT=17, SF=13, CY=6, (none)=2
- Sections: 14; divisions: 86; sub-headings: 47

## Method
- `page` is the folio printed in the book (checked equal to PDF index + 1 on every page that prints one).
- Text is read from the book's native text layer (span alpha 255); the invisible OCR layer (alpha 0) is used
  only on pages without native text (cover, adverts). Run with `--layer ocr` to parse the OCR layer instead.
- Numeric/unit tokens go through OCR normalisation (O->0, l/I->1, S->5, comma decimal, split decimals,
  E/C/M/LF/CY/SF/FT variants); a token already well-formed is never altered.
- A row is exported only when it carries a printed labor unit, or a unit letter beside an item; text-only lines
  inside tables (column sub-headers, group labels, items left blank) are listed below, not exported.
- `heading` = bold-italic centred sub-heading under the division; `table_title` = bold table title
  [+ ` | Note: ...` printed under it]; `raw` = the printed line, including the Rev flag `X` when present.

## Monotonicity violations (difficult < normal or very_difficult < difficult): 12
- p.163 [26 05 19: Low-Voltage Electrical Power Conductors and Cables] Mechanical Terminal Lugs - Two Hole / 750 kcmil: 1.35 / 1.69 / 1.03  <- `750 kcmil 1.35 1.69 1.03 E`
- p.171 [26 05 19: Low-Voltage Electrical Power Conductors and Cables] 3/C 600 Volt Aluminum Overhead Service Drop Cable / #1: 36.00 / 45.00 / 5.00  <- `#1 36.00 45.00 5.00 M`
- p.212 [26 05 33: Raceway and Boxes for Electrical Systems] PVC Coated Steel Offset Nipples | Note: PVC coating repair not included / 1/2-inch: 0.25 / 0.31 / 0.27  <- `1/2-inch 0.25 0.31 0.27 E`
- p.276 [26 05 83: Wiring Connections] Power Connections to Equipment Installed by Others - Aluminum 600 Volt Conduit / 300 Amp Circuits 500 kcmil: 1.20 / 2.00 / 1.90  <- `300 Amp Circuits 500 kcmil 1.20 2.00 1.90 E`
- p.276 [26 05 83: Wiring Connections] Power Connections to Equipment Installed by Others - Aluminum 600 Volt Conduit / 400 Amp Circuits 1000 kcmil: 2.00 / 1.88 / 2.25  <- `400 Amp Circuits 1000 kcmil 2.00 1.88 2.25 E`
- p.276 [26 05 83: Wiring Connections] Power Connections to Equipment Installed by Others - Aluminum 600 Volt Conduit / 450 Amp Circuits 2/300: 2.30 / 2.25 / 2.70  <- `450 Amp Circuits 2/300 2.30 2.25 2.70 E`
- p.353 [26 51 00: Interior Lighting] Lay-in (T-Bar) Fixtures - with Lens / Slave Fixture Labor Deduct (per Fixture): -0.15 / -0.19 / -0.23  <- `Slave Fixture Labor Deduct (per Fixture) -0.15 -0.19 -0.23 E`
- p.356 [26 51 00: Interior Lighting] Fluorescent Ballast / 8-foot Lamp: 0.75 / 0.60 / 0.75  <- `8-foot Lamp 0.75 0.60 0.75 E`
- p.402 [28 05 37: Distributed Antenna System] Security Access Control Systems / Fiber Remote: 3.00 / 2.50 / 3.00  <- `Fiber Remote X 3.00 2.50 3.00 E`
- p.440 [33 71 00: Electrical Utility Transmission and Distribution] Concrete Man Holes Base, Cover and Riser - Excludes Excavation and Gravel Base / 36-inch X 36-inch LID: 1.25 / 1.75 / 1.25  <- `36-inch X 36-inch LID 1.25 1.75 1.25 E`
- p.440 [33 71 00: Electrical Utility Transmission and Distribution] Concrete Man Holes Base, Cover and Riser - Excludes Excavation and Gravel Base / 48-inch X 60-inch LID: 3.50 / 3.00 / 3.50  <- `48-inch X 60-inch LID 3.50 3.00 3.50 E`
- p.453 [34 41 00: Roadway Signaling and Control Equipment]  / Banding Iron Clamps: 0.20 / 5.00 / 0.75  <- `Banding Iron Clamps X 0.20 5.00 0.75 E`

## Pages with a table header but 0 rows: 7
65, 71, 272, 461, 462, 463, 464

## Rows with fewer/more than 3 numbers: 1
- p.200: `Add for Knockout in Blank Box E` -> {}

## Rows without unit: 2
- p.195: `X 0.00 0.00 0.00`
- p.309: `5000 Amp 12.00 15.00 18.00`

## Rows with unrecognised tokens in the numeric zone: 0

## Rows without item description: 5
- p.145: `50.00 62.00 73.00 M`
- p.179: `2.00 2.50 3.00 E`
- p.183: `26.00 32.50 39.00 C`
- p.195: `X 0.00 0.00 0.00`
- p.196: `0.81 1.01 1.22 E`

## Text-only lines inside tables (not exported: no labor unit printed): 17
- p.150 [Teck Connectors | Note: Throat sizes vary with cable and connector manufacturers.]: `Throat Cable`
- p.155 [Solid THHN Conductors]: `Solid Twisted Shielded Pairs`
- p.221 [Wiremold Product - 1500 Series]: `1546B Duplex. Receptacle Box`
- p.270 [Schedule 80 PVC Conduit Laid In Trenches - 10-foot & 20-foot Lengths with Glued Couplings]: `6-inch`
- p.271 [Link Seals Conduit Environmental Sealing Device | Notes: Labor units for hole drilling and coring found in Section 8: Division 26 - Electrical under 25 05 29: Hangers and Supports for Electrical Systems Conduit trade sizes are based on outside diameters for these devices]: `6- inch`
- p.271 [Link Seals Conduit Environmental Sealing Device | Notes: Labor units for hole drilling and coring found in Section 8: Division 26 - Electrical under 25 05 29: Hangers and Supports for Electrical Systems Conduit trade sizes are based on outside diameters for these devices]: `6- inch`
- p.271 [Link Seals Conduit Environmental Sealing Device | Notes: Labor units for hole drilling and coring found in Section 8: Division 26 - Electrical under 25 05 29: Hangers and Supports for Electrical Systems Conduit trade sizes are based on outside diameters for these devices]: `6- inch`
- p.341 [Pole/Tower Interior]: `Average 13.25 Feet per Minute`
- p.344 [Battery Spacesaver System]: `3-Wide Pallets Are Stackable Up to 8 high`
- p.354 [Linear: Pendent, Stem or Aircraft Cable Mounted]: `*not including emergency sections, these should be estimated separately`
- p.354 [Linear: Recessed Mounted]: `*not including emergency sections, these should be estimated separately`
- p.360 [Power Pack with Dual Heads]: `Photoluminescent`
- p.360 [Power Pack with Dual Heads]: `Tritium Self Luminous`
- p.364 []: `7000 to 12000 BTU`
- p.381 [Splicing]: `Splice Tray`
- p.390 [Audio Visual Systems - Programming and Switching]: `Matrix Switcher Programming`
- p.390 [Audio Visual Systems - Programming and Switching]: `Matrix Switcher (Video)`

## Stray unit letters on an empty row (not exported): 1
- p.309: `E`

## Sub-headings (column `heading`): 47
- p.47: `Lightning Protection`
- p.180: `Irreversible Compression Ground System`
- p.190: `Miscellaneous Bolts, Washers, Nuts & Screws`
- p.192: `Hole Drilling and Coring`
- p.192: `Firestop Material`
- p.194: `Rigid Steel Conduit (GRC or GRS) and Fittings`
- p.202: `Electrical Metallic Tubing (EMT) and Fittings`
- p.204: `Intermediate Metal Conduit (IMC) and Fittings`
- p.205: `Rigid Aluminum Conduit and Fittings`
- p.210: `Flexible Steel Conduit (FSC or Greenfield) and Fittings`
- p.210: `Liquidtight Flexible Conduit and Fittings (Sealtite)`
- p.211: `PVC Coated Rigid Steel Conduit`
- p.214: `PVC Rigid Conduit`
- p.216: `Fiberglass Conduit`
- p.217: `Electrical Non-Metallic Flexible Tubing (ENT) Conduit`
- p.218: `Liquid Non-Metallic Flexible Tubing (LNT) Conduit`
- p.220: `Metallic Surface Raceways`
- p.222: `Nonmetallic Surface Raceways`
- p.226: `Metal Wireway`
- p.233: `Steel Tray 3-inch Depth`
- p.234: `Steel Tray 4-inch Depth`
- p.236: `Steel Tray 6-inch Depth`
- p.237: `Steel Cable Tray Fittings & Accessories`
- p.239: `Aluminum Tray 3-inch Depth`
- p.240: `Aluminum Tray 4-inch Depth`
- p.242: `Aluminum Tray 6-inch Depth`
- p.243: `Aluminum Cable Tray Fittings & Accessories`
- p.246: `Fiberglass Tray 3-Inch Depth`
- p.247: `Fiberglass Tray 4-inch Depth`
- p.249: `Fiberglass Tray 6-inch Depth`
- p.250: `Fiberglass Cable Tray Fittings & Accessories`
- p.252: `Solid/Ventilated Steel Tray 3-inch Depth`
- p.253: `Solid/Ventilated Steel Tray 4-inch Depth`
- p.254: `Solid/Ventilated Steel Tray 6-inch Depth`
- p.255: `Solid/Ventilated Steel Cable Tray Fittings & Accessories`
- p.257: `Solid/Ventilated Aluminum Tray 3-inch Depth`
- p.258: `Solid/Ventilated Aluminum Tray 4-inch Depth`
- p.260: `Solid/Ventilated Aluminum Tray 6-inch Depth`
- p.261: `Solid/Ventilated Aluminum Cable Tray Fittings & Accessories`
- p.267: `Trench Duct`
- p.273: `Conduit Tags`
- p.296: `Mission Critical Busway`
- p.310: `Cable Bus`
- p.337: `Generator Sets`
- p.363: `Germicidal Lighting`
- p.453: `Traffic Light Camera Controls`
- p.456: `Maintenance and Protection of Traffic`

## Items whose description spans two lines around the numbers (joined): 49
- p.181: `3-inch Long Steel Structure Aluminum Compress Connector to 1/4-inch to 1/2-inch Thick Steel Flange`
- p.181: `3-inch Long Steel Structure Aluminum Compress Connector to 1/2-inch to 1/4-inch Thick Steel Flange`
- p.181: `6-inch Long Steel Structure Aluminum Compress Connector to 1/4-inch to 1/2-inch Thick Steel Flange`
- p.181: `6-inch Long Steel Structure Aluminum Compress Connector to 1/2-inch to 1/4-inch Thick Steel Flange`
- p.310: `Typical Cross Section 800A`
- p.310: `1200A`
- p.310: `1600A`
- p.310: `2000A`
- p.310: `2500A`
- p.310: `3000A`
- p.310: `4000A`
- p.310: `5000A`
- p.310: `6000A`
- p.311: `Horizontal Installation 800A`
- p.311: `1200A`
- p.311: `1600A`
- p.311: `2000A`
- p.311: `2500A`
- p.311: `3000A`
- p.311: `4000A`
- p.311: `5000A`
- p.311: `6000A`
- p.312: `Vertical Installation 800A`
- p.312: `1200A`
- p.312: `1600A`
- p.312: `2000A`
- p.312: `2500A`
- p.312: `3000A`
- p.312: `4000A`
- p.312: `5000A`
- p.312: `6000A`
- p.313: `Termination Box 800A`
- p.313: `1200A`
- p.313: `1600A`
- p.313: `2000A`
- p.313: `2500A`
- p.313: `3000A`
- p.313: `4000A`
- p.313: `5000A`
- p.313: `6000A`
- p.314: `Environmental Seal 800A`
- p.314: `1200A`
- p.314: `1600A`
- p.314: `2000A`
- p.314: `2500A`
- p.314: `3000A`
- p.314: `4000A`
- p.314: `5000A`
- p.314: `6000A`

## Titles whose first line is not bold (joined): 1
- p.200: `Conduit Body (Condulet) Covers - Steel, Aluminum, PVC, PVC Coated` + `(includes gasket when required)`

## Division names wrapped on two lines (joined): 4
- p.384: `27 16 00: Communications Connecting Cords, Devices and Adapters`
- p.388: `27 31 00: Voice Communications Switching and Routing Equipment`
- p.401: `28 05 00: Common Work Results for Electronic Safety and Security`
- p.443: `33 77 00: Medium-Voltage Utility Switchgear and Protection Devices`

## Notes continued on a plain line: 3
- p.335: `- www.prosolar.com (Primarily for Residential)`
- p.335: `- www.unirac.com`
- p.335: `- www.sunlink.com`

## Pages without a printed folio (PDF index+1 used): 14
1, 24, 38, 44, 56, 62, 68, 372, 398, 412, 428, 448, 458, 531

## Rows per section
- Section 10: Division 28—Electronic Safety and Security: 196
- Section 11: Division 31—Earthwork: 145
- Section 12: Division 32—Exterior Improvements: 40
- Section 13: Division 33—Utilities: 515
- Section 14: Division 34—Transportation: 163
- Section 15: Division 48—Electrical Power Generation: 13
- Section 1: Division 01—General Requirements: 177
- Section 2: Division 03—Concrete: 10
- Section 3: Division 11—Equipment: 7
- Section 4: Division 13—Special Construction: 223
- Section 5: Division 21—Fire Suppression: 96
- Section 7: Division 23—Heating, Ventilating and Air Conditioning (HVAC): 255
- Section 8: Division 26—Electrical: 12234
- Section 9: Division 27—Communications: 482
