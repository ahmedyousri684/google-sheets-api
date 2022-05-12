import gspread
import pandas as pd

gc = gspread.service_account(filename='secret_key.json')




#Placeholders in the sheets
PHONE_NUMBER = 3
ORDER_STATUS = 23
#Placeholders in messangerbot sheet
BOT_PHONE_NUMBER = 0
PSID = 1

def get_phone_by_psid(psid):
    '''
    Get phone number by psid
    response:
    phone number
    '''
    sh = gc.open("Woody Ordering System")
    messange_bot = sh.worksheet("messanger-bot")
    messange_bot_df = pd.DataFrame(messange_bot.get_all_values())
    check_psid = messange_bot_df.loc[messange_bot_df[1] == psid]
    if len(check_psid) > 0:
        print(check_psid)
        formated_phone = check_psid[0].values[0]
        return formated_phone.replace(" ","").replace("-","").replace("(","").replace(")","")
    else:
        return "PSID not exist!"
def get_status(phone):
    '''
    Get status by phone number 
    response:
    Ready to be delevierd 
    Shipped out
    '''
    #reformat the phone number (01x) xxx-xx-xxx
    phone = "("+str(phone[:3])+")"+" "+str(phone[3:6])+"-"+str(phone[6:8])+"-"+str(phone[8:])
    # laser = sh.worksheet("ToLaser")
    # laser_df = pd.DataFrame(laser.get_all_values())
    # # laser_df.columns = laser_df.loc[0,:].values
    sh = gc.open("Woody Ordering System")
    shipped = sh.worksheet("Shipped")
    shipped_df = pd.DataFrame(shipped.get_all_values())
    # shipped_df.columns = shipped_df.loc[0,:].values

    # deliverd = sh.worksheet("Done")
    # deliverd_df = pd.DataFrame(deliverd.get_all_values())
    # # deliverd_df.columns = deliverd_df.loc[0,:].values
    design = sh.worksheet("ToDesign")
    design_df = pd.DataFrame(design.get_all_values())
    # design_df.columns = design_df.loc[0,:].values

    cancelled = sh.worksheet("Cancelled")
    cancelled_df = pd.DataFrame(cancelled.get_all_values()) 
    check_phone = design_df.loc[design_df[PHONE_NUMBER] == phone]
    sheets=[shipped_df]
    flag = ""
    if len(check_phone) > 0:
        #User is found
        # print("User is found")
        #check if order is cancelled or not
        check_cancelled = cancelled_df.loc[cancelled_df[PHONE_NUMBER] == phone]
        if len(check_cancelled) > 0:
            #User is found in cancelled orders 
            if len(check_cancelled) == 1:
                if check_cancelled[ORDER_STATUS].values == '':
                    return "Order is cancelled"
            elif len(check_cancelled) > 1:
                if check_cancelled.iloc[-1][ORDER_STATUS] == '':
                    return "Order is cancelled"   
        # print("Order not cancelled")
        #check if order is designed or not
        if len(check_phone) == 1:
            if check_phone[ORDER_STATUS].values == 'Designed':
                flag = "Order is designed"
                # print("Order is Designed")
            else:
                return "Ordered is confirmed"
        elif len(check_phone) > 1:
            if check_phone.iloc[-1][ORDER_STATUS] == 'Designed':
                flag = "Order is designed"
                # print("Order is Designed")
            else:
                return "Ordered is confirmed"

        #order is designed and ready to be deleiverd
        if flag == "Order is designed":
            # print("order is designed and ready to be deleiverd")
            for sheet in sheets:
                record = sheet.loc[sheet[PHONE_NUMBER] == phone]
                if len(record) < 1:
                    return "Ready to be deleiverd"
                if len(record) == 1:
                    if record[ORDER_STATUS].values == '':
                        return "Ready to be deleiverd"
                    else:
                        return record[ORDER_STATUS].values
                elif len(record) > 1:
                    if record.iloc[-1][ORDER_STATUS] == '':
                        if sheet == shipped_df:
                            return "Ready to be deleiverd"
                    else:
                        return record.iloc[-1][ORDER_STATUS]
    else:
        return "Not found"

def turn_on_tracking(phone, psid):
    '''
    Turn on tracking notification 
    '''
    #reformat the phone number (01x) xxx-xx-xxx
    phone = "("+str(phone[:3])+")"+" "+str(phone[3:6])+"-"+str(phone[6:8])+"-"+str(phone[8:])
    sh = gc.open("Woody Ordering System")
    design = sh.worksheet("ToDesign")
    design_df = pd.DataFrame(design.get_all_values())
    # design_df.columns = design_df.loc[0,:].values
    record = design_df.loc[design_df[PHONE_NUMBER] == phone]
    messange_bot = sh.worksheet("messanger-bot")
    messange_bot_df = pd.DataFrame(messange_bot.get_all_values())
    check_phone = messange_bot_df.loc[messange_bot_df[0] == phone]
    if len(record) > 0:
        if len(check_phone) > 0:
            #phone already added we only update psid
            messange_bot_df.loc[messange_bot_df[0] == phone,1] = psid
            messange_bot.update([] + messange_bot_df.values.tolist())
            return "PSID is updated"
        else:
            messange_bot_df.loc[-1] = [phone, psid]
            messange_bot_df.index = messange_bot_df.index + 1
            messange_bot_df = messange_bot_df.sort_index()
            messange_bot.update([] + messange_bot_df.values.tolist())
            return "Notification is turned on"
    else:
        return "User not found!"
