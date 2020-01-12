from app import app

@app.template_filter()
def add_number_suffix(value):
    # https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    suf = lambda n: "%s"%({1:"st",2:"nd",3:"rd"}.get(n if n<20 else n%10,"th"))
    return suf(value)