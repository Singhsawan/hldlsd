import re
async def validate_q(q):
    query = q

    # It removes the year from the search query.
    query = re.sub(r"[1-2]\d{3}", "", query)
    query = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|hd|movie|hindi|dubbed|dedo|print|full|bhai|season||episode||dubbed|animated|Best|top|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)", "", query.lower(), flags=re.IGNORECASE)

    return query.strip()
