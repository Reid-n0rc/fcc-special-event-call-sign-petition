# Counts call signs in the petition's proposed extended formats, after exclusions, for Table 2.
from collections import defaultdict
U=set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); L25=U-{"X"}; D=set("0123456789"); SYM=L25|D
ALL=U|D; INF=99
def c(chars): return set(chars)
def rng(a,b): return {chr(x) for x in range(ord(a),ord(b)+1)}
A=[
 [(c("KNW"),1,1),(D,1,1),(SYM,3,4),(L25,1,1)],
 [(c("KNW"),1,1),(D,2,INF),(SYM,0,INF),(L25,1,1)],
]
B=[
 [(c("A"),1,1),(rng("A","L"),1,1),(D,2,INF),(SYM,0,INF),(L25,1,1)],
 [(c("KNW"),1,1),(U,1,1),(D,2,INF),(SYM,0,INF),(L25,1,1)],
]
anyseq=(ALL,0,INF)
EXCL={
 "translator": [[(c("KW"),1,1),(D,2,2),(U,2,3)], [(c("KW"),1,1),(D,3,3),(U,2,2)]],
 "SOS/Q":      [[anyseq,(c("S"),1,1),(c("O"),1,1),(c("S"),1,1),anyseq],
                [anyseq,(c("Q"),1,1),(rng("R","U"),1,1),(U,1,1),anyseq]],
 "EMA":        [[(c("AKNW"),1,1),(c("F"),1,1),anyseq,(c("E"),1,1),(c("M"),1,1),(c("A"),1,1),anyseq]],
 "KP/NP/WP":   [[(c("KNW"),1,1),(c("P"),1,1),(c("06789"),1,1),anyseq]],
 "blocks":     [[(c("K"),1,1),(c("A"),1,1),(rng("2","9"),1,1),anyseq]]+
               [[(c("K"),1,1),(c(p[0]),1,1),(c(p[1]),1,1),anyseq] for p in ("C4","C6","G4","L9","X6")],
 "2x3-type prefixes, 3-char suffix": [
   [(c("A"),1,1),(rng("A","L"),1,1),(D,2,INF),(L25,1,1),(SYM,1,1),(L25,1,1)],
   [(c("N"),1,1),(U,1,1),(D,2,INF),(L25,1,1),(SYM,1,1),(L25,1,1)],
   [(c("W"),1,1),(c("CKMRT"),1,1),(D,2,INF),(L25,1,1),(SYM,1,1),(L25,1,1)]],
}
KW=c("KW")
S2302=[  # 47 CFR 2.302 table formats (letters/digits only)
 [(KW,1,1),(U,2,2)], [(KW,1,1),(U,2,2),(D,1,3)], [(KW,1,1),(U,3,3)], [(KW,1,1),(U,3,3),(D,1,2)],
 [(KW,1,1),(U,1,1),(D,4,4)], [(KW,1,1),(U,2,2),(D,4,5)], [(KW,1,1),(U,4,4)], [(KW,1,1),(U,3,3),(D,4,4)],
 [(KW,1,1),(D,2,2),(U,2,2)], [(KW,1,1),(U,1,1),(D,1,1),(c("X"),1,1),(U,2,2)],
 [(c("K"),1,1),(D,4,4)], [(c("W"),1,1),(c("T"),1,1),(D,7,7)], [(c("W"),1,1),(U,2,3)],
]
def closure(p, st):
    out=set(st); stack=list(st)
    while stack:
        i,k=stack.pop()
        if i<len(p) and k>=p[i][1]:
            n=(i+1,0)
            if n not in out: out.add(n); stack.append(n)
    return frozenset(out)
def step(p, st, ch):
    return closure(p,{(i,k+1) for i,k in st if i<len(p) and ch in p[i][0] and k<p[i][2]})
def count(accept, exclude, L):
    ps=accept+exclude; na=len(accept)
    dist=defaultdict(int); dist[tuple(closure(p,{(0,0)}) for p in ps)]=1
    for _ in range(L):
        nd=defaultdict(int)
        for key,n in dist.items():
            for ch in ALL:
                k=tuple(step(p,s,ch) for p,s in zip(ps,key))
                if any(k[:na]): nd[k]+=n
        dist=nd
    acc=lambda p,s:(len(p),0) in s
    return sum(n for key,n in dist.items()
               if any(acc(p,s) for p,s in zip(ps[:na],key[:na]))
               and not any(acc(p,s) for p,s in zip(ps[na:],key[na:])))
if __name__=="__main__":
    allex=[p for v in EXCL.values() for p in v]
    rows=[]
    for L in range(4,8):
        a0,b0=count(A,[],L),count(B,[],L)
        a,b=count(A,allex,L),count(B,allex,L)
        ov=count(A+B,[],L)-count(A+B,S2302,L)
        rows.append((L,a,b))
        print(f"L={L} A {a0:,}->{a:,} (-{a0-a:,})  B {b0:,}->{b:,} (-{b0-b:,})  overlap with 2.302 formats: {ov:,}")
        for name,pats in EXCL.items():
            ra=a0-count(A,pats,L); rb=b0-count(B,pats,L)
            if ra or rb: print(f"     {name}: A -{ra:,} B -{rb:,}")
    ta=sum(r[1] for r in rows); tb=sum(r[2] for r in rows)
    print(f"totals A {ta:,} B {tb:,} all {ta+tb:,} ratio {(ta+tb)/750:,.1f}; <=5: {sum(r[1]+r[2] for r in rows if r[0]<=5):,} ratio {sum(r[1]+r[2] for r in rows if r[0]<=5)/750:,.1f}")
