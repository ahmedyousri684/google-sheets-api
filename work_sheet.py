import gspread
import pandas as pd


gc = gspread.service_account(filename='secret_key.json')




#Placeholders in the sheets
PHONE_NUMBER = 3
ORDER_STATUS = 23
#Placeholders in messangerbot sheet
BOT_PHONE_NUMBER = 0
PSID = 1
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
    check_phone = design_df.loc[design_df[PHONE_NUMBER] == phone]
    sheets=[shipped_df]
    if len(check_phone) > 0:
        #User is found
        for sheet in sheets:
            record = sheet.loc[sheet[PHONE_NUMBER] == phone]
            if len(record) < 1:
                return "Ready to be deleiverd"
            if len(record) == 1:
                print("Record:",record)
                print("Status:", record[ORDER_STATUS].values)
                if record[ORDER_STATUS].values == '':
                    return "Ready to be deleiverd"
                else:
                    return record[ORDER_STATUS].values
            elif len(record) > 1:
                print("Status:", record.iloc[-1][ORDER_STATUS])
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
    if len(record) > 0:
        messange_bot_df.loc[-1] = [phone, psid]
        messange_bot_df.index = messange_bot_df.index + 1
        messange_bot_df = messange_bot_df.sort_index()
        messange_bot.update([] + messange_bot_df.values.tolist())
        return "Notification is turned on"
    else:
        return "User not found!"

turn_on_tracking("01018719246","1029764548")