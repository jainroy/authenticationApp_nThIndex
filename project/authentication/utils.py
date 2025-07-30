class Util:
    @staticmethod
    def send_sms(data):
        print(f"Sending OTP {data['otp']} to phone {data['phone']}")
