"""A kolam on a 3 x 3 grid of dots: nine dots, one unbroken thread.
The thread runs on the diagonals between dots; where two strands meet between two dots they either cross or turn back
(a 'wall'). kolam(walls) traces the loops; find() lists wall sets that leave exactly one loop."""
import itertools, math
N = 3
MID = {'N': (.5, 0), 'E': (1, .5), 'S': (.5, 1), 'W': (0, .5)}
ORDER = ['N', 'E', 'S', 'W']
OPP = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
STEP = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}


def edge_key(i, j, side):
    """a name for the edge between cell (i,j) and its neighbour on `side`; None on the outer boundary"""
    di, dj = STEP[side]; a, b = (i, j), (i + di, j + dj)
    if not (0 <= b[0] < N and 0 <= b[1] < N): return None
    return tuple(sorted([a, b]))


INTERIOR = sorted({edge_key(i, j, s) for i in range(N) for j in range(N) for s in ORDER} - {None})


def trace(walls):
    """walls: set of interior edges where strands turn back. Returns loops as lists of (cell, frm, to)."""
    seen, loops = set(), []
    for i in range(N):
        for j in range(N):
            for a in range(4):
                frm, to = ORDER[a], ORDER[(a + 1) % 4]
                if ((i, j), frozenset((frm, to))) in seen: continue
                loop, cur = [], ((i, j), frm, to)
                while True:
                    (ci, cj), f, t = cur
                    key = ((ci, cj), frozenset((f, t)))
                    if key in seen: break
                    seen.add(key); loop.append(cur)
                    ek = edge_key(ci, cj, t)
                    if ek is None or ek in walls:      # turn back inside the same cell
                        k = ORDER.index(t); nxt = [ORDER[(k + 1) % 4], ORDER[(k - 1) % 4]]; nxt.remove(f)
                        cur = ((ci, cj), t, nxt[0])
                    else:                               # cross into the neighbour, keep the direction
                        di, dj = STEP[t]; ni, nj = ci + di, cj + dj; ent = OPP[t]
                        dx = MID[t][0] - MID[f][0]; dy = MID[t][1] - MID[f][1]
                        k = ORDER.index(ent)
                        for cand in (ORDER[(k + 1) % 4], ORDER[(k - 1) % 4]):
                            if abs((MID[cand][0] - MID[ent][0]) - dx) < 1e-9 and abs((MID[cand][1] - MID[ent][1]) - dy) < 1e-9:
                                cur = ((ni, nj), ent, cand)
                loops.append(loop)
    return loops


def rot(e):  # rotate an edge a quarter turn about the centre
    r = lambda c: (N - 1 - c[1], c[0])
    return tuple(sorted([r(e[0]), r(e[1])]))


def flip(e):
    f = lambda c: (N - 1 - c[0], c[1])
    return tuple(sorted([f(e[0]), f(e[1])]))


def symmetry(walls):
    w = frozenset(walls); s = []
    if frozenset(rot(e) for e in w) == w: s.append('C4')
    elif frozenset(rot(rot(e)) for e in w) == w: s.append('C2')
    if frozenset(flip(e) for e in w) == w: s.append('mirror')
    return s


def find():
    out = []
    for k in range(len(INTERIOR) + 1):
        for ws in itertools.combinations(INTERIOR, k):
            if len(trace(set(ws))) == 1: out.append((symmetry(ws), ws))
    return out


def path(walls, u=100.0, ox=0.0, oy=0.0):
    """SVG path data for the thread: straight diagonals through crossings, quarter-circle arcs round the dots at turns."""
    loops = trace(set(walls)); r = u * .5 / math.sqrt(2); ds = []
    for loop in loops:
        pts = []
        for (ci, cj), f, t in loop:
            mx = (MID[f][0] + MID[t][0]) / 2; my = (MID[f][1] + MID[t][1]) / 2
            pts.append(((ci + mx) * u + ox, (cj + my) * u + oy, (ci, cj)))
        d = [f'M{pts[0][0]:.2f},{pts[0][1]:.2f}']
        for k in range(1, len(pts) + 1):
            x, y, c = pts[k % len(pts)]; px, py, pc = pts[k - 1]
            if c == pc:      # same dot: an arc round it. sweep by the turn direction
                cx, cy = (c[0] + .5) * u + ox, (c[1] + .5) * u + oy
                cr = (px - cx) * (y - cy) - (py - cy) * (x - cx)
                d.append(f'A{r:.2f},{r:.2f} 0 0 {1 if cr > 0 else 0} {x:.2f},{y:.2f}')
            else: d.append(f'L{x:.2f},{y:.2f}')
        ds.append(' '.join(d) + ' Z')
    return ' '.join(ds), len(loops)


def dots(u=100.0, ox=0.0, oy=0.0):
    return [((i + .5) * u + ox, (j + .5) * u + oy) for j in range(N) for i in range(N)]


if __name__ == '__main__':
    res = find(); print(len(res), 'single-thread kolams of', 2 ** len(INTERIOR))
    best = [r for r in res if r[0]]
    from collections import Counter
    print(Counter(tuple(r[0]) for r in res))
    for sym, ws in sorted(best, key=lambda r: (-len(r[0]), len(r[1])))[:14]: print(sym, len(ws), ws)
