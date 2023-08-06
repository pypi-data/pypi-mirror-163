import time

import log
import pomace

from . import Script


class DonJr(Script):

    URL = "http://donjr.com"

    def run(self, page) -> pomace.Page:
        person = pomace.fake.person

        log.info(f"Beginning iteration as {person}")
        page.fill_email_address(person.email_address)
        page = page.click_submit(delay=0.5)
        if "Thank you" in page:
            page = page.click_close(wait=0)

        log.info("Browsing books")
        page = page.click_shop_all()

        log.info("Choosing book")
        page.click_book()

        log.info("Buying book")
        page = page.click_buy_it_now(delay=2, wait=5)

        if "Contact information" not in page:
            log.info("Resetting checkout form")
            page = page.click_change()

        log.info("Checking out")
        page.fill_email(person.email)

        time.sleep(1)
        modal = pomace.shared.browser.find_by_id("shopify-pay-modal")
        if modal and modal.visible:
            log.warn("Handling payment modal")
            page.type_shift_tab()
            page.type_enter()

        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_address(person.address)
        page.type_enter()

        field = page.fill_zip_code.locator.find()
        if field and field.value:
            page = page.click_continue_to_shipping(delay=1, wait=5)
        else:
            log.error("Incomplete address detected")
            return page

        log.info("Continuing to payment")
        page = page.click_continue_to_payment()

        log.info("Completing order")
        page.click_paypal()

        return page.click_complete_order()

    def check(self, page) -> bool:
        return "paypal" in page.url


class TruthSocial(Script):

    URL = "https://truthsocial.com"

    def run(self, page) -> pomace.Page:
        pomace.shared.client.clear_cookies()
        person = pomace.fake.person

        log.info(f"Beginning iteration as {person}")
        page = page.click_register()

        if "birth date" in page:
            page.select_year("1980")
            page = page.click_next(wait=1)

        page.fill_email(person.email)
        return page.click_next(wait=1)

    def check(self, page) -> bool:
        return "We sent you an email" in page
