"""
스모크 테스트.

repository 가 실제 엑셀에서 데이터를 잘 읽는지 빠르게 확인한다.
실행:
  cd backend
  python _smoke_test.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# .env 로드
from dotenv import load_dotenv  # noqa: E402

load_dotenv(Path(__file__).parent / ".env")

from app.data.excel_loader import preloadAll  # noqa: E402
from app.repositories.document_repository import (  # noqa: E402
    findAllDocuments,
    findDocumentByNo,
    findDocumentsByTag,
    findTagsByDocument,
)
from app.repositories.manufacture_repository import (  # noqa: E402
    findAllManufactures,
    findManufactureByName,
)
from app.repositories.tag_repository import (  # noqa: E402
    findAllTags,
    findTagByNo,
    findTagsByPackage,
    listPackageNames,
    listSystemNames,
)
from app.services.hierarchy_service import (  # noqa: E402
    listPackagesBySystem,
    listSystems,
)
from app.services.search_service import searchAll  # noqa: E402


def printSection(title: str) -> None:
    print()
    print("=" * 6, title, "=" * 6)


def main() -> int:
    printSection("preloadAll")
    print(preloadAll())

    printSection("findAllTags (count + first 3)")
    tags = findAllTags()
    print("count:", len(tags))
    for t in tags[:3]:
        print(" -", t.tagNo, "|", t.description, "|", t.systemName, "/", t.packageName)

    printSection("findTagByNo('P-1001')")
    detail = findTagByNo("P-1001")
    print(detail.model_dump() if detail else None)

    printSection("listSystemNames / listPackageNames")
    systems = listSystemNames()
    print("systems:", systems)
    print("packages of first system:", listPackageNames(systems[0]) if systems else [])

    printSection("findTagsByPackage('A')")
    pkgTags = findTagsByPackage("A")
    print("count:", len(pkgTags), "first:", pkgTags[0].tagNo if pkgTags else None)

    printSection("findAllDocuments")
    docs = findAllDocuments()
    print("count:", len(docs))
    print("sample:", docs[0].model_dump() if docs else None)

    printSection("findDocumentByNo('ABCD-ZL-0001')")
    doc = findDocumentByNo("ABCD-ZL-0001")
    print(doc.model_dump() if doc else None)

    printSection("findDocumentsByTag('P-1001')")
    docsByTag = findDocumentsByTag("P-1001")
    for d in docsByTag:
        print(" -", d.documentNo, "|", d.documentName, "|", d.revision)

    printSection("findTagsByDocument('ABCD-ZL-0001') (first 5)")
    tagsByDoc = findTagsByDocument("ABCD-ZL-0001")
    print("count:", len(tagsByDoc), "first 5:", tagsByDoc[:5])

    printSection("findAllManufactures (count + first 3)")
    mans = findAllManufactures()
    print("count:", len(mans))
    for m in mans[:3]:
        print(" -", m.companyName, "|", m.industrySector, "|", m.countryOrigin)

    printSection("findManufactureByName('Nexus Marine')")
    one = findManufactureByName("Nexus Marine")
    print(one.model_dump() if one else None)

    printSection("hierarchy listSystems / listPackagesBySystem")
    sys_nodes = listSystems()
    for s in sys_nodes:
        print(" -", s.systemName, "packages:", s.packageCount)
    if sys_nodes:
        pkgs = listPackagesBySystem(sys_nodes[0].systemName)
        print(" first system packages:", [(p.packageName, p.tagCount) for p in pkgs])

    printSection("searchAll('P-1001')")
    for h in searchAll("P-1001", limit=10):
        print(" -", h.hitType, "|", h.key, "|", h.label)

    printSection("searchAll('Production')")
    for h in searchAll("Production", limit=5):
        print(" -", h.hitType, "|", h.key, "|", h.label)

    return 0


if __name__ == "__main__":
    sys.exit(main())
