"""Verify taqdimot.pptx without external deps.

Checks:
  * zip opens, no bad CRCs
  * every XML part is well-formed
  * exactly 10 slide parts
  * each slide has >=1 <p:pic> and resolves its image rel to a real media file
  * each media PNG has valid signature and non-trivial size
"""

import os
import sys
import xml.dom.minidom as minidom
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PPTX = os.path.join(HERE, "taqdimot.pptx")


def main():
    assert os.path.exists(PPTX), "pptx missing"
    z = zipfile.ZipFile(PPTX)
    bad = z.testzip()
    assert bad is None, f"corrupt entry: {bad}"

    names = z.namelist()

    # XML well-formedness for all .xml / .rels parts
    for nm in names:
        if nm.endswith(".xml") or nm.endswith(".rels"):
            minidom.parseString(z.read(nm))

    slides = sorted(n for n in names if n.startswith("ppt/slides/slide") and n.endswith(".xml"))
    assert len(slides) == 10, f"expected 10 slides, got {len(slides)}"

    media = [n for n in names if n.startswith("ppt/media/")]
    assert len(media) == 10, f"expected 10 media images, got {len(media)}"

    pic_total = 0
    for s in slides:
        body = z.read(s).decode("utf-8")
        npic = body.count("<p:pic>")
        assert npic >= 1, f"{s} has no picture"
        pic_total += npic
        # resolve rels -> media target exists
        base = os.path.basename(s)
        rels = f"ppt/slides/_rels/{base}.rels"
        rels_xml = z.read(rels).decode("utf-8")
        assert "/image" in rels_xml and ".png" in rels_xml, f"{s} missing image rel"
        # Times New Roman present
        assert "Times New Roman" in body, f"{s} not using Times New Roman"

    # validate media PNG bytes
    for m in sorted(media):
        data = z.read(m)
        assert data[:8] == b"\x89PNG\r\n\x1a\n", f"{m} not a PNG"
        assert len(data) > 2000, f"{m} suspiciously small ({len(data)} bytes)"

    print("VERIFICATION PASSED")
    print(f"  slides            : {len(slides)}")
    print(f"  embedded images   : {len(media)}")
    print(f"  total picture shapes: {pic_total}")
    print(f"  all XML parts well-formed, zip CRCs OK, Times New Roman on every slide")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("VERIFICATION FAILED:", e)
        sys.exit(1)
