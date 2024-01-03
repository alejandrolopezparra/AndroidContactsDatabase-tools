#!/usr/bin/env python2

#
# acdb2vcf.py is a python tool by alejandrolopezparra to export contacts data from Android Contacts
# Databases (SQLite3) to vCard 3.0 text files. It's useful to recover contacts data from an Android
# Phone (contacts2.db) into Google Contacts or other services supporting vCard file format (.vcf).
# 
# acdb2vcf.py v1.0 supports:
#   - Python 2/3
#   - Android Contacts Database format (SQLite3)
#   - Account type filtering: Google, Exchange, WhatsApp, Telegram, Phone, SIM, ...
#   - N, FN, ADR, BDAY, EMAIL, NOTE, ORG, ROLE, TEL properties from vCard 3.0 standard
#
# It's based on the original tool and instructions by Andreas Boehler at
#  https://www.aboehler.at/doku/doku.php/blog:2012:1007_recovering_contacts_from_dead_android_phone
#
# It's also based on modifications by Ian Worthington at
#  https://forum.xda-developers.com/android/help/extract-contacts-backup-t3307684
#
# More info about Android Contacts Database at:
#  - Android Contacts Database Structure - https://www.dev2qa.com/android-contacts-database-structure/
#  - Contacts Provider - https://developer.android.com/guide/topics/providers/contacts-provider
#
# More info about vCard 3.0 at:
#  - vCard 3.0 format specification - https://www.evenx.com/vcard-3-0-format-specification
#  - A MIME Content-Type for Directory Information - https://tools.ietf.org/html/rfc2425
#  - vCard MIME Directory Profile - https://tools.ietf.org/html/rfc2426.html
#  - Representing vCard Objects in RDF - https://www.w3.org/Submission/2010/SUBM-vcard-rdf-20100120/
#  - vCard (Wikipedia) - https://en.wikipedia.org/wiki/VCard
#
# Changelog:
#  * 1.0 (2018-11-06)
#    - Initial release
#

import sqlite3
import sys
import codecs

# VERSION
version = "1.0"

account_types = {}
# ????????: 'vnd.sec.contact.agg.account_type'account_types = {}
account_types['exchange'] = "'com.google.android.gm.exchange'"
account_types['google']   = "'com.google'"
account_types['imap']     = "'com.google.android.gm.legacyimap'"
account_types['phone']    = "'vnd.sec.contact.phone'"
account_types['sim']      = "'vnd.sec.contact.sim'"
account_types['telegram'] = "'org.telegram.messenger'"
account_types['tuenti']   = "'com.tuenti.messenger.auth'"
account_types['twitter']  = "'com.twitter.android.auth.login'"
account_types['whatsapp'] = "'com.whatsapp'"


# Usage information
def usage(filename):
    help_string = "\n"
    help_string += filename + " v" + version + " is a python tool by alejandrolopezparra to export contacts\n"
    help_string += "data from Android Contacts Databases (contacts2.db) to vCard 3.0 files (.vcf)\n"
    help_string += "\n"
    help_string += "usage: " + filename + " [options] <db_input> <vcf_output>\n"
    help_string += "\n"
    help_string += "Arguments:\n"
    help_string += "  [options]\n"
    help_string += "     --all\tAll contacts will be exported. By default\n"
    for key in account_types:
        help_string += "     --" + key + "\t" + key.capitalize() + " contacts will be exported\n"
    help_string += "\n"
    help_string += "  <db_input>\tInput Android Contact Database (SQLite3), e.g. contacts2.db\n"
    help_string += "  <vcf_output>\tOutput Virtual Contact File (vCard) filename, e.g. MyContacts.vcf\n"
    sys.exit(help_string)


# Remove Line Breaks from strings
def removeLB (text):
    if text != None:
        text = text.replace("\n"," ")
        text = text.replace("\r"," ")
    return text

# Contact class stores contacts data
class Contact:
    def __init__(self, id):
        self.id = id
        self.phoneNumbers = []
        self.mailAddresses = []
        self.addresses = []
        self.name = ""
        self.lastname = ""
        self.firstname = ""
        self.org = ""
        self.role = ""
        self.note = ""
        self.bday = ""

    def AddPhone(self, number):
        if number != None:
            self.phoneNumbers.append(removeLB(number))

    def GetPhones(self):
        return self.phoneNumbers

    def AddMail(self, mail):
        if mail != None:
            self.mailAddresses.append(removeLB(mail))

    def GetMails(self):
        return self.mailAddresses

    def AddAddress(self, address):
        if address != None:
            self.addresses.append(removeLB(address))

    def GetAddresses(self):
        return self.addresses

    def SetFirstname(self, firstname):
        if firstname != None:
            self.firstname = removeLB(firstname)

    def SetLastname(self, lastname):
        if lastname != None:
            self.lastname = removeLB(lastname)

    def SetName(self, name):
        if name != None:
            self.name = removeLB(name)

    def GetName(self):
        return (self.name, self.lastname, self.firstname)

    def SetNote(self, note):
        if note != None:
            self.note = removeLB(note)

    def GetNote(self):
        return (self.note)

    def SetBirthday(self, bday):
        if bday != None:
            self.bday = removeLB(bday)

    def GetBirthday(self):
        return (self.bday)

    def SetOrg(self, org):
        if org != None:
            self.org = removeLB(org)

    def GetOrg(self):
        return (self.org)

    def SetRole(self, role):
        if role != None:
            self.role = removeLB(role)

    def GetRole(self):
        return (self.role)

    def GetId(self):
        return self.id

    def GetVCard(self):
        vcard = []
        # HEADER
        vcard.append("BEGIN:VCARD")
        vcard.append("VERSION:3.0")
        # N:
        vcard.append("N:" + self.lastname + ";" + self.firstname)
        # FN:
        fnText = "?"
        if self.name != "":
            fnText = self.name
        elif len(self.lastname) > 0 and len(self.firstname) > 0:
            fnText = self.firstname + " " + self.lastname
        elif len(self.lastname) > 0:
            fnText = self.lastname
        elif len(self.firstname) > 0:
            fnText = self.firstname
        vcard.append("FN:" + fnText)
        # TEL;
        for phone in self.phoneNumbers:
            vcard.append("TEL;" + phone)
        # EMAIL;
        for mail in self.mailAddresses:
            vcard.append("EMAIL;" + mail)
        # ADR;
        for address in self.addresses:
            vcard.append("ADR;" + address)
        # ORG:
        if self.org:
            vcard.append("ORG:" + self.org)
        # ROLE:
        if self.role:
            vcard.append("ROLE:" + self.role)
        # NOTE:
        if self.note:
            vcard.append("NOTE:" + self.note)
        # BDAY:
        if self.bday:
            vcard.append("BDAY:" + self.bday)
        vcard.append("END:VCARD")
        return vcard

###########
# MAIN code
###########

#
# 1. Parsing arguments
#

# Executable File Name
efn = sys.argv[0]

# Checking number of arguments
arg_n = len(sys.argv)
#print "arg_n: " + str(arg_n)
if arg_n < 3:
    print(" * Error message: There are less arguments than expected")
    usage(efn)
elif arg_n > 12:
    print(" * Error message: There are more arguments than expected")
    usage(efn)

# Input and OutPut File Names are the last 2 arguments
ifn = sys.argv[arg_n-2]
#print "ifn: " + ifn
ofn = sys.argv[arg_n-1]
#print "ofn: " + ofn

# Checking options
options = {}
for arg in sys.argv:
    type = arg.replace("--","",1)
    #print "type: " + type
    if type in account_types or type == "all":
    #print "options[" + type + "]: " + arg
        options[type] = arg
    elif arg in (efn, ifn, ofn):
        pass
    else:
        print(" * Error message: option '" + arg + "' is not valid")
        usage(efn)


#
# 2. Extracting contacts data from database
#

# Building account type filter based on options
account_filter = ""
if 'all' not in options:
   #print "all is not present so filters may be applied"
   i = 0
   for key in list(options.keys()):
      #print "key: " + key
      if key in account_types:
          i += 1
          account_type=account_types[key]
          if i == 1:
             account_filter += " WHERE account_type=" + account_type
          else:
             account_filter += " OR account_type=" + account_type
#print "account_filter: " + account_filter

# Connecting to database
db = sqlite3.Connection(ifn)
c = db.cursor()

# Getting accounts for chosen account types
c.execute("SELECT _id, account_name FROM accounts" + account_filter)
accounts = {}
while True:
    account = c.fetchone()
    if account is None: break
    if account[0] not in accounts:
        accounts[account[0]] = account[1]

# Getting contacts for selected accounts
contacts = {}
for key in list(accounts.keys()):
    id_filter=" WHERE account_id=" + str(key)

    c.execute("SELECT COUNT(*) FROM raw_contacts" + id_filter)
    num_entries = c.fetchone()[0]
    print(" * Getting " + str(num_entries) + " contacts from " + str(accounts[key]) + " (account_id = " + str(key) + ")")

    c.execute("SELECT _id FROM raw_contacts" + id_filter)
    while True:
        row = c.fetchone()
        if row is None: break
        if row[0] not in contacts:
            contacts[row[0]] = Contact(row[0])

# Getting data for selected contacts
for key in list(contacts.keys()):
    c.execute("SELECT mimetype_id, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10 FROM data WHERE raw_contact_id = " + str(contacts[key].GetId()))
    while True:
        row = c.fetchone()
        if row is None: break
        mimetype = row[0] if row[0] else ""
        data1    = row[1] if row[1] else ""
        data2    = row[2] if row[2] else ""
        data3    = row[3] if row[3] else ""
        data4    = row[4] if row[4] else ""
        data5    = row[5] if row[5] else ""
        data6    = row[6] if row[6] else ""
        data7    = row[7] if row[7] else ""
        data8    = row[8] if row[8] else ""
        data9    = row[9] if row[9] else ""
        data10   = row[10] if row[10] else ""
        if mimetype == 1: # Mail
            email = data1
            contacts[key].AddMail("type=INTERNET;type=WORK:" + data1)
        elif mimetype == 4: # ORG and ROLE
            org      = data1
            org_unit = data5
            role     = data4
            if org or org_unit:
                contacts[key].SetOrg(org + ";" + org_unit)
            if role:
                contacts[key].SetRole(role)
        elif mimetype == 5: # Phone
            phone_number      = data1
            phone_number_cc   = data4
            phone_type        = data2  
            phone_type_string = "type=WORK:" # Work, by default
            if phone_type == "1" and len(phone_number)>8: # Home
                phone_type_string="type=HOME:"
            elif phone_type == "2" and len(phone_number)>8: # Mobile
                phone_type_string="type=CELL:"
            contacts[key].AddPhone(phone_type_string + phone_number)
        elif mimetype == 7: # Name
            name       = data1
            first_name = data2
            last_name  = data3
            contacts[key].SetName(name)
            contacts[key].SetFirstname(first_name)
            contacts[key].SetLastname(last_name)
        elif mimetype == 8: # Address
            address_type = data2
            street       = data4
            locality     = data7
            region       = data8
            postalCode   = data9
            country      = data10
            address_type_string = "type=WORK:" # Work, by default
            if address_type == "1": # Home
                address_type_string = "type=HOME:"
            contacts[key].AddAddress(address_type_string + ";;" + street + ";" + locality + ";" + region + ";" + postalCode + ";" + country)
        elif mimetype == 11: # Note
            note = data1
            contacts[key].SetNote(note)
        elif mimetype == 12: # Birth day
            bday = data1
            contacts[key].SetBirthday(bday)
        elif mimetype == 21: # Telegram Profile
            phone_number      = data3
            telegram_id       = data1
            phone_type_string="type=CELL:"
            contacts[key].AddPhone(phone_type_string + phone_number)


# Closing database connetions
c.close()
db.close()


#
# 3. Exporting contacts data to vCard file (.VCF)
#

if contacts:
    fp = codecs.open(ofn, "w", "utf-8")
    fp.write('\ufeff')
    #print "Contact's Details: "
    for key in list(contacts.keys()):
        if contacts[key].GetId() != 0:
            #string = ""
            #last, first = contacts[key].GetName()
            #if len(last) > 0 and len(first) > 0:
            #    string += last + " " + first
            #elif len(last) > 0:
            #    string += last
            #elif len(first) > 0:
            #    string += first
            #phones = contacts[key].GetPhones()
            #for phone in phones:
            #    string += phone + " "
            #mails = contacts[key].GetMails()
            #for mail in mails:
            #    string += mail + " "
            #print string
            fp.write("\n".join(contacts[key].GetVCard()))
            fp.write("\n")
    fp.close()
