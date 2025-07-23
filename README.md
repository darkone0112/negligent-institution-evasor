# AppointmentChecker Builder

This tool helps you build and configure the AppointmentChecker application into a standalone executable.

## Prerequisites

- Python 3.x installed
- Access to command line/terminal
- Internet connection (for installing dependencies)

## Quick Start

1. Clone this repository
2. Run the build script:
```bash
python build.py
```

## Detailed Usage

### First Time Setup

When you run the build script for the first time or without a `config.json` file, it will:

1. Launch a configuration GUI asking for:
   - NIE (Spanish Foreigner ID Number)
   - Name
   - Surname
   - Nationality

2. After entering your information and clicking "Save Configuration", it will:
   - Create a `config.json` file with your information
   - Start building the executable

### Build Process

The build script will:

1. Check for existing configuration
2. Install PyInstaller if not already installed
3. Build the executable with all required dependencies
4. Copy the configuration file to the distribution folder

### Output Files

After successful build, you'll find these files in the `dist` folder:
```
dist/
  ├── AppointmentChecker.exe  # The main executable
  └── config.json             # Your configuration file
```

### Important Notes

- **Always keep** `config.json` in the same folder as the executable
- You can edit `config.json` manually if you need to change your information
- The JSON structure must be maintained:
```json
{
    "personal_info": {
        "nie": "YOUR_NIE",
        "name": "YOUR_NAME",
        "surname": "YOUR_SURNAME",
        "nationality": "YOUR_NATIONALITY"
    }
}
```

### Updating Configuration

If you need to create a new configuration:
1. Delete the existing `config.json`
2. Run `python build.py` again
3. The GUI will appear to create a new configuration

### Troubleshooting

1. **Missing config.json**: 
   - The GUI will appear automatically to create one

2. **Build Errors**: 
   - Make sure you have Python installed
   - Check your internet connection
   - Try running `pip install pyinstaller` manually

3. **Runtime Errors**:
   - Verify `config.json` is in the same folder as the executable
   - Check if `config.json` has the correct format
   - Make sure all values in `config.json` are properly filled

## License

See the LICENSE file for details.  
## Automating what should never have needed automation
**Because Spain’s Extranjería made it clear they don’t give a damn, so we automated their job.**

If you’ve tried booking a NIE appointment online, you already know:  
It’s not just broken, it’s **hostile by design**.

The official site is a Kafkaesque hellloop of dropdowns, captchas, and fake availability.  
It gaslights you with “No appointments available” 24/7, then magically offers dozens to shady resellers and bots.

This isn’t bad code.  
This is **systemic negligence wrapped in HTML**.  
A digital middle finger to every foreigner trying to do things legally.

So we said **fuck that**, and wrote a bot.

---

## 🤖 What this does

- Clicks through the portal like a tired, desperate human would  
- Picks your province, office, and trámite  
- Waits like a person. Scrolls like a person. Doesn’t crash like the site.  
- Alerts you the second something shows up  
- Leaves no trace. No spam. Just justice.

---

## 💢 Why this matters

Because people lose jobs, visas, and peace of mind because **a public institution refused to do the bare minimum**.

Because the only people who get appointments are:  
1. Lucky  
2. Rich  
3. Using bots  

Let’s make sure the third one isn’t exclusive to mafias.

---

## 🚫 What this isn’t

- It’s not a scam.  
- It’s not for sale.  
- It’s not polite.

This is a **code-based middle finger** to a broken system that abandoned the people it’s supposed to serve.

---

## ⚠️ Final note

This project is a **protest**.  
Use it with respect. Don’t scalp appointments. Don’t profit from others' desperation.  
This is here so **you don’t get steamrolled by indifference**.

If they ever fix the system, we’ll gladly shut this down. But let’s be honest…  
They won’t.

---

> **Negligent Institution Evasor — automating what should never have needed automation.**
>  
> *Built out of desperation. Maintained out of spite.*
