from tools.http import req_get


async def get_all_markets():
    return await req_get("http://44.204.6.181:81/api/markets/attention/")
