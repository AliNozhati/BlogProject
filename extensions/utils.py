from . import jalali
from django.utils import timezone

# تبدیل کردن اعداد انگلیسی به فارسی
def persian_number(mystr):
    # اعداد سمت راست باید فارسی شود
    numbers = {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
    }

    # جابجا کردن اعداد
    for e, p in numbers.items():
        mystr = mystr.replace(e, p)

    return mystr

# تبدیل تاریخ میلادی به شمسی
def jalali_converter(time):
    time = timezone.localtime(time)
    jmonths = ["اسفند","بهمن" ,"دی","آذر","آبان","مهر","شهریور","مرداد", "تیر", "خرداد", "اردیبهشت", "فروردین"]
    time_to_list = list(jalali.Gregorian(f"{time.year},{time.month},{time.day}").persian_tuple())

    for index, month in enumerate(jmonths):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    out = f"{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}، ساعت {time.hour}:{time.minute}"
    return persian_number(out)
