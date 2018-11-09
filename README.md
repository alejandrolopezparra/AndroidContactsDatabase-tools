# Android Contacts Database tools
Tools to extract data from *Android Contacts Database* (*SQLite3*). By default, it's located at */data/data/com.android.providers.contacts/databases/contacts2.db* although some manufacturers may change it.

The easy way to get *contacts2.db* is using [*adb*](https://developer.android.com/studio/releases/platform-tools) tool:
   ```bash
   $# adb pull /data/data/com.android.providers.contacts/databases/contacts2.db
   ```

More information about *Android Contacts Database* can be found on:
- [Android Contacts Database Structure](https://www.dev2qa.com/android-contacts-database-structure/)
- [Contacts Provider](https://developer.android.com/guide/topics/providers/contacts-provider)


## [acdb2vcf.py](https://github.com/alejandrolopezparra/AndroidContactsDatabase-tools/blob/master/acdb2vcf.py)
*Python* tool by [*alejandrolopezparra*](https://github.com/alejandrolopezparra) to export contacts data from *Android Contacts Databases* (*SQLite3*) to *vCard 3.0* text files. It's useful to recover contacts data from an *Android* phone (*contacts2.db*) into *Google Contacts* or other services supporting *vCard* file format (.vcf).

*acdb2vcf.py* v1.0 supports:
- *Android Contacts Database* format (*SQLite3*).
- Account type filtering: *Google*, *Exchange*, *WhatsApp*, *Telegram*, *Phone*, *SIM*, ...
- N, FN, ADR, BDAY, EMAIL, NOTE, ORG, ROLE, TEL properties from *vCard 3.0* standard.

*acdb2vcf.py* v1.0 depends on:
- *Python 2* by default but *Python 3* is also supported.
- *sqlite3* *Python* module.

### Usage
```
acdb2vcf.py [options] <db_input> <vcf_output>

Arguments:
  [options]
     --all	All contacts will be exported. By default
     --google	Google contacts will be exported
     --exchange	Exchange contacts will be exported
     --telegram	Telegram contacts will be exported
     --twitter	Twitter contacts will be exported
     --phone	Phone contacts will be exported
     --tuenti	Tuenti contacts will be exported
     --whatsapp	Whatsapp contacts will be exported
     --imap	Imap contacts will be exported
     --sim	Sim contacts will be exported

  <db_input>	Input Android Contact Database (SQLite3), e.g. contacts2.db
  <vcf_output>	Output Virtual Contact File (vCard) filename, e.g. MyContacts.vcf
```

### Additional info
It's based on the original tool and instructions by _Andreas Böhler_ on https://www.aboehler.at/doku/doku.php/blog:2012:1007_recovering_contacts_from_dead_android_phone

It's also based on modifications by _Ian Worthington_ on https://forum.xda-developers.com/android/help/extract-contacts-backup-t3307684

Information about *vCard 3.0* can be found at:
- [vCard 3.0 format specification](https://www.evenx.com/vcard-3-0-format-specification)
- [RFC2425: A MIME Content-Type for Directory Information](https://tools.ietf.org/html/rfc2425)
- [RFC2426: vCard MIME Directory Profile](https://tools.ietf.org/html/rfc2426.html)
- [Representing vCard Objects in RDF](https://www.w3.org/Submission/2010/SUBM-vcard-rdf-20100120/)
- [Wikipedia: vCard](https://en.wikipedia.org/wiki/VCard)
