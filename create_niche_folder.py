import os
from pathlib import Path
from typing import List, Dict, Tuple

# --- CONFIGURATION ---

# Base path - change this to your desired location
# NOTE: Using a cross-platform path structure in the script
BASE_PATH = r"/mnt/c/Users/rosselio/Documents"

# Niche-Specific Directory and File Templates
# The folder structure is tailored for the core workflows of each niche.

# 1. E-Commerce: Focus on Inventory, Marketing, and Fulfillment
ECOMMERCE_DIRS = [
    "1_ecom_inventory/product_catalogs",
    "1_ecom_inventory/supplier_info",
    "2_ecom_marketing/social_media_assets",
    "2_ecom_marketing/email_campaigns",
    "3_ecom_orders/fulfillment_logs",
    "3_ecom_orders/returns_data",
    "4_ecom_support/customer_service_scripts",
    "5_ecom_analytics/reports"
]

# 2. Real Estate: Focus on Lead Management and Transactions
REAL_ESTATE_DIRS = [
    "1_re_crm/lead_lists",
    "1_re_crm/follow_up_scripts",
    "2_re_listings/marketing_assets", # Photos, Video, etc.
    "2_re_listings/mls_data",
    "3_re_transactions/contracts_docs",
    "3_re_transactions/inspection_reports",
    "3_re_transactions/closing_checklists",
    "4_re_admin/agent_templates"
]

# 3. Bookkeeper: Focus on Monthly Close and Compliance
BOOKKEEPER_DIRS = [
    "1_bk_monthly_close/bank_statements",
    "1_bk_monthly_close/receipts_source_data",
    "2_bk_compliance/tax_docs",
    "3_bk_ar_ap/accounts_receivable", # Invoices sent
    "3_bk_ar_ap/accounts_payable", # Bills to pay
    "4_bk_reports/monthly_pnl_bs",
    "5_bk_admin/client_onboarding"
]

# 4. Travel Agent Booking: Focus on Itineraries and Vendor Management
TRAVEL_AGENT_DIRS = [
    "1_ta_intake/client_preferences",
    "2_ta_research/flight_options",
    "2_ta_research/hotel_options",
    "3_ta_itinerary/drafts",
    "3_ta_itinerary/final_confirmations",
    "4_ta_vendors/supplier_contacts",
    "5_ta_marketing/promo_materials"
]

COMMON_FILES = {
    "README.md": (
        lambda name, niche: 
        f"# 📁 VA Client Project: {name} ({niche})\n\n"
        f"--- \n\n"
        f"## 📋 Quick Links & Logins \n\n"
        f"**Master SOP:** [Link to Niche SOP]\n\n"
        f"**Client CRM:** [Link to CRM]\n\n"
        f"## ✅ Monthly/Weekly Checklists \n\n"
        f"- [ ] Monthly Invoicing\n"
        f"- [ ] Weekly Report Generation\n"
    ),
    "0_Client_Logins_SECURE.txt": (
        lambda name, niche:
        "# IMPORTANT: Store sensitive data in a secure Password Manager (e.g., LastPass, 1Password) ONLY.\n"
        "# Use this file only for non-sensitive notes or temporary links.\n"
    ),
    "0_Niche_SOP.md": (
        lambda name, niche: 
        f"## Standard Operating Procedure for {niche} Clients\n\n"
        f"1. **Start of Day:** Check the 'CRITICAL' task list in project management tool.\n"
        f"2. **Real Estate Example:** Every Monday, review Transaction Coordination deadlines.\n"
        f"3. **Bookkeeping Example:** Every 1st-5th of the month, begin the **Monthly Close** process.\n"
    ),
}

NICHE_OPTIONS: Dict[str, Tuple[str, List[str]]] = {
    "1": ("E-Commerce", ECOMMERCE_DIRS),
    "2": ("Real Estate", REAL_ESTATE_DIRS),
    "3": ("Bookkeeper", BOOKKEEPER_DIRS),
    "4": ("Travel Agent Booking", TRAVEL_AGENT_DIRS)
}

# --- FUNCTIONS ---

def get_niche_selection() -> Tuple[str, List[str]]:
    """Displays the niche selection menu and validates the user's choice."""
    print("\n--- 💻 Project Niche Selection ---")
    for key, (name, _) in NICHE_OPTIONS.items():
        print(f"| {key}. {name}")
    print("---------------------------------")
    
    while True:
        choice = input("Enter the number for the client's niche: ").strip()
        if choice in NICHE_OPTIONS:
            return NICHE_OPTIONS[choice]
        print("❌ Invalid selection. Please enter a number from the list.")

def create_project_structure(
    project_path: Path, 
    main_folder: str, 
    niche_name: str, 
    directories: List[str]
):
    """Creates the directories and files for the selected niche."""
    print(f"\n📁 Creating project: {main_folder} ({niche_name})")
    print(f"📍 Location: {project_path.absolute()}")
    print("-" * 60)
    
    # Create main project folder
    project_path.mkdir(exist_ok=True)
    
    # 1. Create all subdirectories
    for directory in directories:
        dir_path = project_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Dir: {directory}")

    # 2. Create additional files
    for filename, content_func in COMMON_FILES.items():
        file_path = project_path / filename
        content = content_func(main_folder, niche_name)
        
        # Ensure parent dir exists (though should be main_folder here)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Only create if it doesn't exist
        if not file_path.exists(): 
            file_path.write_text(content, encoding='utf-8')
            print(f"📄 File: {filename}")
        
    print("-" * 60)
    print(f"🎉 Project '{main_folder}' for '{niche_name}' created successfully!")
    print(f"📂 Location: {project_path.absolute()}")

def create_project_with_verification():
    """Main function to guide the user through project creation."""
    
    # 1. Verify base path exists
    base_path = BASE_PATH
    if not base_path.exists():
        print(f"⚠️ Base path does not exist: {base_path}")
        try:
            base_path.mkdir(parents=True)
            print(f"✅ Created base path: {base_path}")
        except OSError as e:
            print(f"❌ Failed to create base path: {e}")
            return
    
    # 2. Get niche selection
    try:
        niche_name, directories_to_create = get_niche_selection()
    except Exception:
        # Handle case where selection fails (e.g., interrupted input)
        print("\nOperation cancelled or selection failed.")
        return

    # 3. Get main folder name (Client Name)
    while True:
        main_folder = input(f"\nEnter the **Client Name** for the {niche_name} project (e.g., Smith Realty): ").strip()
        if main_folder:
            # Simple check for basic invalid characters
            invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
            if any(char in main_folder for char in invalid_chars):
                print("❌ Folder name contains invalid characters. Please use letters, numbers, and spaces.")
                continue
            break
        print("❌ Folder name cannot be empty. Please try again.")
    
    # Full path where everything will be created
    project_path = base_path / main_folder
    
    # 4. Check if main folder already exists
    if project_path.exists():
        response = input(f"⚠️ Folder '{main_folder}' already exists. Overwrite/Continue? (y/n): ").lower()
        if response != 'y':
            print("Operation cancelled.")
            return

    # 5. Create the project structure
    try:
        create_project_structure(project_path, main_folder, niche_name, directories_to_create)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred during creation: {e}")
        return
        
    # 6. Offer to open the folder
    if os.name == 'nt': # Windows OS
        try:
            open_explorer = input("\nOpen folder in File Explorer? (y/n): ").lower()
            if open_explorer == 'y':
                os.startfile(project_path)
        except Exception:
            # Fails on non-Windows/Linux with os.startfile
            pass
    
# Run the function
if __name__ == "__main__":
    create_project_with_verification()
