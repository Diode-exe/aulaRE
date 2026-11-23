import hid

VID = 0x38A6
PID = 0x28F1

target_path = None
for dev in hid.enumerate(VID, PID):
    if dev['usage_page'] == 0xFFB0:
        target_path = dev['path']
        break

if not target_path:
    raise RuntimeError("Could not find IF:2 (UP:0xffb0)")

d = hid.device()
d.open_path(target_path)

# Send 9 pages (0x00 to 0x08) with leading Report ID 0x00 (65 bytes total!)
for page in range(9):
    header = bytes([0x00, 0x05, 0x04, 0x00, page])  # Report ID 0x00 + 05 04 00 <page>
    # green blue red
    leds = bytes([0x00, 0xFF, 0x00, 0xFF]) * 15
    written = d.write(header + leds)
    print(f"Page {page}: wrote {written} bytes")

d.close()
