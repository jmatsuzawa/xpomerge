# -*- coding: utf-8 -*-

import sys
from translate.storage.po import pofile

def merge(org, new):
    if org.obsolete: return org
    if org.target == new.target and new.isfuzzy(): return org
    if org.isfuzzy() and new.isfuzzy(): return org

    org.target = new.target
    org.markfuzzy(new.isfuzzy())
    return org

def rm_fuzzy_msgid_cmt(unit):
    src = unit.__str__()
    if (unit.isfuzzy()): return src
    lines = []
    for line in src.split("\n"):
        if line[:2] == '#|': continue
        lines.append(line)
    return "\n".join(lines)


if __name__ == '__main__':
    orgpo = sys.argv[1]
    newpo = sys.argv[2]
    org_units = pofile.parsefile(orgpo).units
    new_units = pofile.parsefile(newpo).units
    new_map = {}
    for unit in new_units:
        if unit.isobsolete(): continue
        new_map[(unit.getcontext(), unit.source)] = unit
    for org in org_units:
        new = new_map.get((org.getcontext(), org.source), None)
        if not new:
            print(org)
            continue
        merged = merge(org, new)
        print(rm_fuzzy_msgid_cmt(merged))
