import nextcord, time
from nextcord.ext import commands
from nextcord.ui import View

from util import db, charge, sim, logging

GUILD_ID = 1048387768054718576

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Game('SMS - KOREAㅣ문의 > DM'), status=nextcord.Status.online)
    print('AutoPhoneVerify By Online')

@bot.slash_command(description=f"잔액 충전하기", guild_ids=[GUILD_ID])
async def 충전(interaction: nextcord.Interaction):
    # 슬래쉬 커맨드 입력 즉시 출력
    await interaction.send(embed=nextcord.Embed (
        title='충전을 시도하는 중 ...',
        description='**```css\n[ 🔎 ] 충전을 시도하고 있습니다...```**'
    ), ephemeral=True)
    # 유저 데이터가 존재하는지 여부를 확인
    result = db.user_data(interaction.user.id) 
    if result == None: # 존재하지 않는 경우 data_create 를 사용하여 유저 데이터를 생성
        db.data_create(interaction.user.id)
        print(f'신규 데이터가 생성됨ㅣ{interaction.user.id}ㅣ{interaction.user.name}')
    # 슬래쉬 커맨드를 입력한 유저에게 디엠 전송
    try:
        msg = await interaction.user.send(embed = nextcord.Embed(title='잔액 충전', description='결제방식을 입력해주세요 ( 문화상품권 / 계좌이체 )'))
        await interaction.edit_original_message(embed= nextcord.Embed(
            title = '충전 알림',
            description= f'**```css\n[ ✅ ] 디엠으로 충전을 위한 메시지가 전송되었습니다!```**'
        ))
    except:
        return await interaction.edit_original_message(embed= nextcord.Embed(
            title = '충전 알림',
            description= f'**```css\n[ ⛔ ] 디엠 전송이 불가능합니다.```**'
        ))
    # 디엠에서 충전 방식을 읽어옴 
    def check(charge_type):
        return (isinstance(charge_type.channel, nextcord.channel.DMChannel) and (interaction.user.id == charge_type.author.id))
    try:
        charge_type = await bot.wait_for('message', timeout=40, check=check)
        charge_type = charge_type.content
    except:
        return await interaction.user.send(embed=nextcord.Embed(title='충전 실패', description='시간 초과'))
    
    if charge_type == '문화상품권':
        return await interaction.user.send(embed=nextcord.Embed(title='충전 실패', description='현재 문화상품권 충전을 지원하지 않습니다.'))

    elif charge_type == '계좌이체':
        try:
            await interaction.user.send(embed = nextcord.Embed(title='잔액 충전', description='입금하실 금액을 입력해주세요 ( EX. 1000 )'))
            charge_amount = await bot.wait_for('message', timeout=300, check=None)
            charge_amount = charge_amount.content
        except:
            return await interaction.user.send(embed=nextcord.Embed(title='충전 실패', description='시간 초과'))

        result = charge.toss_request('SMSKR', charge_amount)

        if result == 'FAIL':
            return await interaction.user.send(embed= nextcord.Embed(
            title='계좌이체 실패 알림',
            description='**```css\n[ ⛔ ] 문제가 발생하였습니다. 관리자에게 문의해주세요.```**'
            ))
        class confirm(nextcord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None
            @nextcord.ui.button(label = '이체확인', style=nextcord.ButtonStyle.green)
            async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
                self.value = True
                self.stop()
        view = confirm()
        await interaction.user.send(embed = nextcord.Embed(
            title='계좌 충전 요청',
            description=f'**사용법**\n```1. 입금자명을 {result[0]} 으로 변경해주세요.\nㄴ 올바르게 변경하지 않은 경우 충전이 실패됩니다.\n2. {result[1]} 로 충전하실 금액을 입금해주세요.\n3. 이체를 완료하신 뒤 아래 버튼을 눌러주세요.\n4. 요청은 5분 후 만료되니 주의해주세요 !```'), view=view)
        await view.wait()
        if view.value:
            con_res = charge.toss_confirm(result[0])
            if con_res[0] == 'FAIL':
                return await interaction.user.send(embed= nextcord.Embed(
                    title='계좌이체 실패 안내',
                    description=f'**```css\n[ ⛔ ] {con_res[1]}```**'
                ))
            user_money = db.add_money(interaction.user.id, con_res[1])
            await interaction.user.send(embed= nextcord.Embed(
                    title='계좌이체 성공 안내',
                    description=f'**```css\n[ ✅ ] {con_res[1]} 원이 성공적으로 충전되었습니다.\n\n고객님의 잔액은 {user_money} 원 입니다.```**'
                ))
            logging.charge_log(interaction.user.id, interaction.user.name, con_res[1])
            

@bot.slash_command(description=f"내 정보 조회하기", guild_ids=[GUILD_ID])
async def 내정보(interaction: nextcord.Interaction):
    await interaction.send(embed= nextcord.Embed (
        title='정보 확인 시도 중 ...',
        description='**```css\n[ 🔎 ] 정보 확인을 시도하고 있습니다...```**'
    ), ephemeral=True)
    result = db.user_data(interaction.user.id)
    if result == None: # 존재하지 않는 경우 data_create 를 사용하여 유저 데이터를 생성
        db.data_create(interaction.user.id)
        print(f'신규 데이터가 생성됨ㅣ{interaction.user.id}ㅣ{interaction.user.name}')
    result = db.user_data(interaction.user.id)
    embed = nextcord.Embed(
        title = '정보 확인 성공 알림',
        description= f'**```css\n[ ✅ ] 정보 확인이 성공적으로 완료되었습니다!\n\n[ 닉네임 ] {bot.get_user(result[0])} 님 \n[ 잔액 ] {result[1]} 원\n[ 구매횟수 ] {result[2]} 회```**'
    )
    await interaction.edit_original_message(embed=embed)

@bot.slash_command(description=f"번호인증하기ㅣ이용 전 이용방법 확인 필수", guild_ids=[GUILD_ID])
async def 번호인증(interaction: nextcord.Interaction, 플랫폼:str):
    await interaction.send(embed= nextcord.Embed (
        title='번호 인증 시도 중 ...',
        description='**```css\n[ 🔎 ] 번호 인증을 시도하고 있습니다...```**'
    ), ephemeral=True)
    objName = {
        "디스코드": {
            "name": "discord",
            "price": "400",
            "country": "russia"
        }, # check 
        "텔레그램": {
            "name": "telegram",
            "price": "700",
            "country": "russia"
        }, # Err 
        "인스타그램": {
            "name": "instagram",
            "price": "400",
            "country": "russia"
        }, # NonCheck
        "페이스북": {
            "name": "facebook",
            "price": "400",
            "country": "russia"
        },
        "넷플릭스": {
            "name": "netflix",
            "price": "300",
            "country": "russia"
        },
        "트위터": {
            "name": "twitter",
            "price": "300",
            "country": "russia"
        },
    }
    result = db.user_data(interaction.user.id)
    if result == None: # 존재하지 않는 경우 data_create 를 사용하여 유저 데이터를 생성
        db.data_create(interaction.user.id)
        print(f'신규 데이터가 생성됨ㅣ{interaction.user.id}ㅣ{interaction.user.name}')

    if not 플랫폼 in objName:
        return await interaction.edit_original_message(embed=nextcord.Embed (
            title='오류 알림',
            description='**```css\n[ ⛔ ] 지원하지 않는 플랫폼이거나 존재하지 않습니다.```**'
        ))
    
    if objName[플랫폼]:
        name = objName[플랫폼]['name']
        price = objName[플랫폼]['price']
        country = objName[플랫폼]['country']
        if int(price) > int(result[1]):
            return await interaction.edit_original_message(embed=nextcord.Embed (
                title='오류 알림',
                description='**```css\n[ ⛔ ] 잔액이 부족합니다. 충전 후 이용해주세요.```**'
            ))
        try:
            await interaction.user.send(embed = nextcord.Embed(title='번호 인증 알림', description=f'{플랫폼} 번호인증을 시작합니다 ...'))
            await interaction.edit_original_message(embed=nextcord.Embed(
                title = '번호 인증 알림',
                description= f'**```css\n[ ✅ ] 디엠으로 번호인증을 위한 메시지가 전송되었습니다!```**'
                ))
            db.sub_money(interaction.user.id, price) # 금액 차감
            req_number = sim.req_buy(name, country)
            logging.buy_log(interaction.user.id, interaction.user.name, 플랫폼)
            try:
                number = req_number['phone']
                country = req_number['country']
                id = str(req_number['id'])
                await interaction.user.send(embed = nextcord.Embed(title='번호 인증 알림', description=f'**```- 주의 : 해당 번호 인증은 5분 뒤 파기됩니다.\n전화번호 : {number}\n국가 : {country}\n- 디엠으로 인증번호가 전송되니 봇의 기능을 사용하지 마시고 대기해주세요.```**'))
                while True:
                    time.sleep(30)
                    print(f'[ 5SIM REQUESTㅣPLATFORM : {플랫폼}ㅣID : {id}ㅣUSER : {interaction.user.name} ]')
                    result_order = sim.req_order(id)
                    if result_order == 'TIMEOUT':
                        await interaction.user.send(embed = nextcord.Embed(title='번호 인증 알림', description=f'**```\n인증번호가 발송되지 않아 제한시간이 종료되었습니다.\n처음부터 다시 진행해주세요.```**'))
                        break
                    if result_order == 'BANNED':
                        await interaction.user.send(embed = nextcord.Embed(title='번호 인증 알림', description=f'**```\n시스템 오류로 번호 인증에 실패하였습니다.```**'))
                        break
                    if not result_order == 'FAIL':
                        await interaction.user.send(embed = nextcord.Embed(title='번호 인증 알림', description=f'**```\n인증번호 : {result_order}```**'))
                        break
                    await interaction.user.send(embed = nextcord.Embed(title='번호 인증 알림', description=f'**```\n인증번호 확인에 실패했습니다.\n30초 뒤 다시 시도합니다.```**'))
            except Exception as e:
                print(e)
                return await interaction.edit_original_message(embed=nextcord.Embed (
                    title='오류 알림',
                    description='**```css\n[ ⛔ ] 서버 오류가 발생하였습니다.```**'
                ))
        except Exception as e:
            print(e)
            return await interaction.edit_original_message(embed=nextcord.Embed (
                title='오류 알림',
                description='**```css\n[ ⛔ ] 디엠이 막혀있습니다.```**'
            ))

bot.run('')