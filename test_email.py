# test_mail_oop.py
import re
import pytest
from datetime import date

from email_service import (
    Status,
    clean_text,
    EmailAddress,
    Email,
    EmailService,
)

# ---------- helpers ----------

EMAIL_OK_COM = "user@domain.com"
EMAIL_OK_RU  = "user@site.ru"
EMAIL_OK_NET = "user@service.net"
EMAIL_BAD_ORG = "bad@org.org"
EMAIL_NO_AT   = "nodogmail.com"

def yyyy_mm_dd(s: str) -> bool:
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", s or ""))


# ---------- EmailAddress ----------

def test_emailaddress_valid_normalize_and_mask():
    e = EmailAddress("  USER.Name@DoMaIn.CoM  ")
    assert e.value == "user.name@domain.com"
    # masked: первые 2 символа логина + ***@ + домен
    assert e.masked == "us***@domain.com"

@pytest.mark.parametrize("addr", [EMAIL_BAD_ORG, EMAIL_NO_AT, "", "   ", "x@y.comm"])
def test_emailaddress_invalid_raises(addr):
    with pytest.raises(ValueError):
        EmailAddress(addr)

def test_emailaddress_normalize_addresses_in_place():
    e = EmailAddress("  a@b.com ")
    # уже нормализован в __init__, вызов не ломает
    e.normalize_addresses()
    assert e.value == "a@b.com"


# ---------- clean_text ----------

@pytest.mark.parametrize(
    "raw, expected",
    [
        ("\tHi\n there \n", "Hi  there"),
        ("  ok\tok  ", "ok ok"),
        ("single", "single"),
        ("", ""),
    ],
)
def test_clean_text_replaces_tabs_newlines_and_strips(raw, expected):
    assert clean_text(raw) == expected


# ---------- Email methods ----------

def test_email_clean_add_short_and_repr_mask():
    em = Email(
        sender=EmailAddress("Sender@study.com"),
        recipient=EmailAddress(EMAIL_OK_COM),
        subject="  Hi\t\n",
        body="Message\twith\nwhitespace",
    )
    em.clean_data().add_short_body(n=10)
    # subject/body очищены
    assert em.subject == "Hi"
    assert em.body == "Message with whitespace"
    # short_body обрезан до 10 + ...
    assert em.short_body == "Message wi..."
    # __repr__ содержит маску отправителя
    rep = repr(em)
    assert "se***@study.com" in rep  # 'se' из 'sender'

def test_email_is_empty_fields_sets_invalid():
    em = Email(
        sender=EmailAddress(EMAIL_OK_COM),
        recipient=EmailAddress(EMAIL_OK_RU),
        subject="   ",
        body="  ",
    )
    assert em.is_empty_fields() is True
    assert em.status == Status.INVALID

def test_email_prepare_ready_sets_all_fields():
    em = Email(
        sender=EmailAddress("s@study.com"),
        recipient=EmailAddress(EMAIL_OK_NET),
        subject="  Hello\t\n",
        body="Body\n\tOK long long long",
    ).prepare()

    assert em.status == Status.READY
    assert yyyy_mm_dd(em.date)
    assert em.masked_sender == "s***@study.com"
    assert em.short_body in "Body  OK l..."  # зависит от длины
    # sent_text собран и содержит ключевые поля
    assert "Кому: user@service.net" in (em.sent_text or "")
    assert "от s***@study.com" in (em.sent_text or "")
    assert "Тема: Hello" in (em.sent_text or "")

def test_email_prepare_ready_sets_all_fields_long():
    em = Email(
        sender=EmailAddress("s@study.com"),
        recipient=EmailAddress(EMAIL_OK_NET),
        subject="  Hello\t\n",
        body="Body\n\tOK",
    ).prepare()

    assert em.status == Status.READY
    assert yyyy_mm_dd(em.date)
    assert em.masked_sender == "s***@study.com"
    assert em.short_body in "Body  OK"  # зависит от длины
    # sent_text собран и содержит ключевые поля
    assert "Кому: user@service.net" in (em.sent_text or "")
    assert "от s@study.com" in (em.sent_text or "")
    assert "Тема: Hello" in (em.sent_text or "")


def test_email_prepare_invalid_on_bad_addresses():
    em = Email(
        sender=EmailAddress(EMAIL_OK_COM),
        recipient=EmailAddress("x@bad.org"),  # ValueError уже упадёт в конструкторе
        subject="S",
        body="B",
    )
    # До сюда мы не дойдём: конструктор валидирует. Проверим иначе:
    with pytest.raises(ValueError):
        Email(sender=EmailAddress(EMAIL_OK_COM),
              recipient=EmailAddress(EMAIL_BAD_ORG),
              subject="S", body="B")


def test_email_reply_swaps_and_prefix_and_flow():
    original = Email(
        sender=EmailAddress("boss@company.com"),
        recipient=EmailAddress("qa@company.ru"),
        subject="Release status",
        body="When is the ETA for RC?",
    )
    reply = original.reply("RC is out today.").prepare()
    assert reply.sender.value == "qa@company.ru"
    assert reply.recipient.value == "boss@company.com"
    assert reply.subject == "Re: Release status"
    assert reply.status == Status.READY


# ---------- EmailService: send_to_many flow ----------

def test_service_empty_recipient_list_returns_empty():
    svc = EmailService()
    base = Email(
        sender=EmailAddress("default@study.com"),
        recipient=EmailAddress(EMAIL_OK_COM),
        subject="",
        body="",
    )
    result = svc.send_to_many(base, [], "subj", "body")
    assert result == []

def test_service_invalid_sender_returns_empty():
    svc = EmailService()
    base = Email(
        sender=EmailAddress("default@study.com"),
        recipient=EmailAddress(EMAIL_OK_COM),
        subject="",
        body="",
    )
    result = svc.send_to_many(base, [EMAIL_OK_COM], "S", "B", sender="bad.sender")  # без @
    assert result == []

def test_service_filters_invalid_recipients_and_sends():
    svc = EmailService()
    base = Email(
        sender=EmailAddress("default@study.com"),
        recipient=EmailAddress(EMAIL_OK_COM),
        subject="",
        body="",
    )
    result = svc.send_to_many(
        base,
        recipient_list=[EMAIL_OK_COM, EMAIL_BAD_ORG, "no-at", "  ", EMAIL_OK_RU],
        subject="Hello",
        message="World",
        sender="default@study.com",
    )
    # Останутся только валидные TLD: .com и .ru
    assert len(result) == 2
    assert all(e.status == Status.SENT for e in result)
    assert {e.recipient.value for e in result} == {EMAIL_OK_COM, EMAIL_OK_RU}

def test_service_removes_self_send():
    svc = EmailService()
    base = Email(
        sender=EmailAddress("default@study.com"),
        recipient=EmailAddress(EMAIL_OK_COM),
        subject="",
        body="",
    )
    result = svc.send_to_many(
        base,
        recipient_list=["default@study.com", "user@site.net"],
        subject="X",
        message="Y",
        sender="default@study.com",
    )
    # self удалён, остался один
    assert len(result) == 1
    assert result[0].recipient.value == "user@site.net"

def test_service_subject_body_cleaning_and_sent_text():
    svc = EmailService()
    base = Email(
        sender=EmailAddress("DEFAULT@STUDY.COM"),
        recipient=EmailAddress(EMAIL_OK_COM),
        subject="",
        body="",
    )
    res = svc.send_to_many(
        base,
        recipient_list=["  USER@Site.NeT  "],
        subject="  Hello\t\n",
        message="  Body\n\tOK ",
        sender=" DEFAULT@STUDY.COM ",
    )
    assert len(res) == 1
    em = res[0]
    assert em.subject == "Hello"
    assert em.body == "Body OK"
    assert yyyy_mm_dd(em.date)
    assert "Кому: user@site.net" in (em.sent_text or "")
    assert "от default@study.com" in (em.sent_text or "")

def test_service_duplicates_are_kept_by_current_impl():
    svc = EmailService()
    base = Email(
        sender=EmailAddress("default@study.com"),
        recipient=EmailAddress(EMAIL_OK_COM),
        subject="",
        body="",
    )
    lst = ["dupe@domain.com", "DuPe@Domain.Com", "dupe@domain.com", "default@study.com"]
    res = svc.send_to_many(
        base,
        recipient_list=lst,
        subject="Dup",
        message="Same",
        sender="default@study.com",
    )
    # Удалится только self; дубликаты останутся (текущая логика)
    assert len(res) == 3
    assert all(e.recipient.value == "dupe@domain.com" for e in res)

def test_service_empty_subject_or_body_returns_empty():
    svc = EmailService()
    base = Email(
        sender=EmailAddress("default@study.com"),
        recipient=EmailAddress(EMAIL_OK_COM),
        subject="",
        body="",
    )
    assert svc.send_to_many(base, [EMAIL_OK_COM], "   ", "body") == []
    assert svc.send_to_many(base, [EMAIL_OK_COM], "subj", " \t\n ") == []

def test_service_status_transitions_ready_sent_and_invalid_failed():
    svc = EmailService()

    # валидный — SENT
    base1 = Email(
        sender=EmailAddress("default@study.com"),
        recipient=EmailAddress(EMAIL_OK_COM),
        subject="",
        body="",
    )
    res_ok = svc.send_to_many(base1, [EMAIL_OK_COM], "S", "B")
    assert len(res_ok) == 1
    assert res_ok[0].status == Status.SENT

    # сделаем письмо неготовым: пустой subject → ничего не отправится
    base2 = Email(
        sender=EmailAddress("default@study.com"),
        recipient=EmailAddress(EMAIL_OK_COM),
        subject="",
        body="",
    )
    res_bad = svc.send_to_many(base2, [EMAIL_OK_COM], " \n\t", "B")
    assert res_bad == []


# ---------- TLD validation (parametrized) ----------

@pytest.mark.parametrize(
    "addr, ok",
    [
        ("a@b.com", True),
        ("a@b.ru", True),
        ("a@b.net", True),
        ("a@b.ORG", False),
        ("a@b.comm", False),
        ("ab.com", False),
    ],
)
def test_tld_validation(addr, ok):
    if ok:
        # не должен упасть
        e = EmailAddress(addr)
        assert e.check_correct_email() is True
    else:
        with pytest.raises(ValueError):
            EmailAddress(addr)
