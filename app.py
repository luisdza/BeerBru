import streamlit as st

# Set the page configuration to wide layout
st.set_page_config(layout="wide")

# Apply custom CSS for improved aesthetics
st.markdown("""
    <style>
        /* Basic container styles for a clean look */
        .container {
            padding: 1.5em;
            border-radius: 8px;
            background-color: #f9f9f9;
            margin-bottom: 2em;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        /* Header styles for larger, clearer headers */
        h1 {
            font-size: 2.5em;
            color: #3e8e41;
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 0;
        }
        h2 {
            color: #2a7f34;
            margin-top: 0;
        }
        .tab-header {
            font-size: 1.2em;
            color: #3e8e41;
        }
        /* Improved font styles */
        body {
            font-family: "Helvetica Neue", Arial, sans-serif;
            color: #333;
        }
        /* Better padding for input fields */
        .stNumberInput, .stTextInput, .stSlider, .stSelectbox {
            margin-bottom: 1em;
        }
    </style>
""", unsafe_allow_html=True)

# BeerBru: Streamlit App for Beer Brewing Calculations
st.title("🍺 BeerBru: Your Brewing Assistant 🍺")

# Introduction to the brewing assistant
st.markdown("""
Welcome to **BeerBru**! This app is your ultimate companion for homebrewing, guiding you through each step with helpful calculations and tips.
Fill in the inputs for your brewing session, and let BeerBru handle the rest. **Happy Brewing!** 🍻
""")

# Create tabs for each step in the brewing process
tabs = st.tabs(["📝 Recipe Details", "🔥 Mashing Process", "💧 Sparging Process", "🍿 Boil & Hop Additions", "🧪 Fermentation", "🧾 Bottling & ABV", "🍯 Yeast & Miscellaneous Additions", "🕒 Timing & Scheduling"])

# Step 1: Recipe Details
with tabs[0]:
    st.header("Step 1: Recipe Details 📝")

    # Input fields for selecting beer style and batch details
    st.write("Choose your beer style, batch size, and grain bill details.")

    # Dropdown for selecting beer style
    beer_style = st.selectbox("Select Beer Style", ["Ale", "Lager", "Stout", "IPA", "Porter", "Pilsner", "Saison", "Wheat Beer"])
    # Input for batch size
    batch_size = st.number_input("Batch Size (Liters)", min_value=1.0, max_value=100.0, value=20.0, step=0.5)
    # Input for total grain weight
    grain_weight = st.number_input("Total Grain Weight (Kilograms)", min_value=0.1, max_value=20.0, value=5.0, step=0.1)
    
    # Grain Bill Input
    st.subheader("Grain Bill")
    # Input for the number of grain types
    num_grains = st.number_input("Number of Grain Types", min_value=1, max_value=10, value=2)
    grains = []
    for i in range(num_grains):
        # Input for each grain type
        grain_type = st.text_input(f"Grain Type {i+1}", key=f"grain_type_{i}")
        # Validation to ensure grain type is not empty
        if grain_type.strip() == "":
            st.warning(f"Grain Type {i+1} cannot be empty.")
            st.stop()
        # Input for the amount of each grain type
        grain_amount = st.number_input(f"Amount of {grain_type} (kg)", min_value=0.0, max_value=10.0, value=0.5, step=0.1, key=f"grain_amount_{i}")
        grains.append((grain_type, grain_amount))

# Step 2: Mashing Process
with tabs[1]:
    st.header("Step 2: Mashing Process 🔥")
    st.write("Control the mash temperature and water-to-grain ratio for optimal starch conversion.")

    # Input for desired mash temperature
    desired_mash_temp = st.slider("Desired Mash Temperature (°C)", 60, 75, 65)
    # Input for water to grain ratio
    water_to_grain_ratio = st.slider("Water to Grain Ratio (L/kg)", 2.0, 4.0, 2.5, step=0.1)

    # Calculations for Mashing
    mash_water_volume = grain_weight * water_to_grain_ratio
    # Strike water temperature calculation (simplified for better readability)
    strike_water_temp = desired_mash_temp + (0.4 * water_to_grain_ratio) - 0.5

    # Display mashing calculations
    st.subheader("Mashing Calculations")
    st.write(f"Optimal Mash Water Volume: **{mash_water_volume:.2f} Liters**")
    st.write(f"Suggested Strike Water Temperature: **{strike_water_temp:.1f} °C**")

    # Allow advanced users to adjust the strike water temperature calculation
    custom_strike_temp = st.checkbox("Customize Strike Water Temperature Calculation")
    if custom_strike_temp:
        strike_water_temp = st.number_input("Custom Strike Water Temperature (°C)", min_value=50.0, max_value=100.0, value=strike_water_temp, step=0.1)

# Step 3: Sparging Process
with tabs[2]:
    st.header("Step 3: Sparging Process 💧")
    st.write("Determine the right sparge water volume to hit your target batch size.")

    # Check if mash water volume exceeds the batch size
    if mash_water_volume > batch_size:
        st.warning("The mash water volume exceeds the total batch size. Adjust the ratio or grain weight.")
        adjust_ratio = st.checkbox("Automatically adjust water-to-grain ratio to fit batch size")
        if adjust_ratio:
            water_to_grain_ratio = batch_size / grain_weight
            mash_water_volume = batch_size  # Adjust mash water volume to fit batch size
            st.write(f"Adjusted Water to Grain Ratio: **{water_to_grain_ratio:.2f} L/kg**")
            st.write(f"Adjusted Mash Water Volume: **{mash_water_volume:.2f} Liters**")
        else:
            sparge_water_volume = 0.0
    else:
        # Calculate sparge water volume
        sparge_water_volume = batch_size - mash_water_volume
        st.write(f"Recommended Sparge Water Volume: **{sparge_water_volume:.2f} Liters**")

# Step 4: Boil & Hop Additions
with tabs[3]:
    st.header("Step 4: Boil & Hop Additions 🍿")
    st.write("Plan hop additions and boil times to achieve the perfect flavor and bitterness.")

    # Input for boil time
    boil_time = st.number_input("Boil Time (Minutes)", min_value=30, max_value=120, value=60)
    boil_duration = boil_time  # Link boil_duration dynamically with boil_time

    # Input for number of hop additions
    num_hops = st.number_input("Number of Hop Additions", min_value=1, max_value=5, value=2)

    hops = []
    for i in range(num_hops):
        # Input for each hop type
        hop_type = st.text_input(f"Hop Type {i+1}", key=f"hop_type_{i}")
        # Validation to ensure hop type is not empty
        if hop_type.strip() == "":
            st.warning(f"Hop Type {i+1} cannot be empty.")
            st.stop()
        # Input for amount of hops
        hop_amount = st.number_input(f"Amount of {hop_type} (grams)", min_value=0.0, max_value=100.0, value=10.0, step=1.0, key=f"hop_amount_{i}")
        # Input for boil time for each hop addition
        hop_time = st.slider(f"Boil Time for {hop_type} (minutes)", 0, int(boil_time), 30, key=f"hop_time_{i}")
        hops.append((hop_type, hop_amount, hop_time))

# Step 5: Fermentation Process
with tabs[4]:
    st.header("Step 5: Fermentation Process 🧪")
    st.write("Set your primary and secondary fermentation conditions.")

    # Input for fermentation temperature
    fermentation_temp = st.slider("Fermentation Temperature (°C)", 15, 25, 20)
    # Input for primary fermentation days
    primary_fermentation_days = st.number_input("Primary Fermentation Days", min_value=5, max_value=14, value=7)
    # Input for secondary fermentation days
    secondary_fermentation_days = st.number_input("Secondary Fermentation Days (if applicable)", min_value=0, max_value=30, value=0)

    # Allow more precise control over conditioning times
    conditioning_days = st.number_input("Conditioning Days (optional)", min_value=0, max_value=60, value=0)

# Step 6: Bottling & ABV Calculation
with tabs[5]:
    st.header("Step 6: Bottling & ABV Calculation 🧾")
    st.write("Calculate the ABV based on the original and final gravity of your brew.")

    # Input for original gravity (OG)
    original_gravity = st.number_input("Original Gravity (OG)", min_value=1.000, max_value=1.200, value=1.050, step=0.001)
    # Input for final gravity (FG)
    final_gravity = st.number_input("Final Gravity (FG)", min_value=0.900, max_value=1.200, value=1.010, step=0.001)
    # Calculate ABV if OG is greater than FG
    if original_gravity > final_gravity:
        abv = (original_gravity - final_gravity) * 131.25
    else:
        st.warning("Original Gravity must be greater than Final Gravity to calculate a valid ABV.")
        st.stop()
        abv = 0.0

    # Display ABV calculation
    st.subheader("Alcohol by Volume (ABV)")
    st.write(f"Estimated ABV: **{abv:.2f}%**")

# Step 7: Yeast & Miscellaneous Additions
with tabs[6]:
    st.header("Step 7: Yeast & Miscellaneous Additions 🍯")
    st.write("Specify yeast strain and any additional ingredients like spices or fruit.")

    # Input for yeast type
    yeast_type = st.text_input("Yeast Strain")
    if yeast_type.strip() == "":
        st.warning("Yeast strain cannot be empty.")
        st.stop()
    # Input for additional ingredients
    num_misc_additions = st.number_input("Number of Miscellaneous Additions", min_value=0, max_value=10, value=0)
    misc_additions = []
    for i in range(num_misc_additions):
        misc_type = st.text_input(f"Miscellaneous Addition {i+1}", key=f"misc_type_{i}")
        if misc_type.strip() == "":
            st.warning(f"Miscellaneous Addition {i+1} cannot be empty.")
            st.stop()
        misc_amount = st.text_input(f"Amount of {misc_type} (e.g., 50g, 1 stick)", key=f"misc_amount_{i}")
        if misc_amount.strip() == "":
            st.warning(f"Amount for {misc_type} cannot be empty.")
            st.stop()
        misc_additions.append((misc_type, misc_amount))

# Step 8: Timing & Scheduling
with tabs[7]:
    st.header("Step 8: Timing & Scheduling 🕒")
    st.write("Plan out the entire brewing schedule, from mashing to bottling.")

    # Input for scheduling details
    brew_day_length = st.slider("Brew Day Length (hours)", 4, 12, 8)
    mash_duration = st.slider("Mash Duration (minutes)", 30, 120, 60)
    boil_duration = st.slider("Boil Duration (minutes)", 30, 120, boil_time)
    fermentation_duration = primary_fermentation_days + secondary_fermentation_days + conditioning_days

    # Display timing summary
    st.subheader("Brewing Schedule Summary")
    st.write(f"**Brew Day Length:** {brew_day_length} hours")
    st.write(f"**Mash Duration:** {mash_duration} minutes")
    st.write(f"**Boil Duration:** {boil_duration} minutes")
    st.write(f"**Total Fermentation Duration:** {fermentation_duration} days")

# Final Summary of the brewing process
st.header("Brewing Summary")
st.write("Here's a quick summary of your brew. 🍻")
# Summary of selected beer style and batch size
st.write(f"**Beer Style:** {beer_style}")
st.write(f"**Batch Size:** {batch_size} L")
# Summary of grain bill
st.write("**Grain Bill:**")
for grain in grains:
    st.write(f"- {grain[0]}: {grain[1]} kg")
# Summary of mash and sparge details
st.write(f"**Water to Grain Ratio:** {water_to_grain_ratio} L/kg")
st.write(f"**Mash Water Volume:** {mash_water_volume:.2f} L")
st.write(f"**Strike Water Temperature:** {strike_water_temp:.1f} °C")
st.write(f"**Sparge Water Volume:** {sparge_water_volume:.2f} L")
# Summary of boil and hop additions
st.write(f"**Boil Time:** {boil_time} minutes")
st.write("**Hop Additions:**")
for hop in hops:
    st.write(f"- {hop[0]}: {hop[1]} grams, added at {hop[2]} minutes")
# Summary of yeast and miscellaneous additions
st.write(f"**Yeast Strain:** {yeast_type}")
if misc_additions:
    st.write("**Miscellaneous Additions:**")
    for misc in misc_additions:
        st.write(f"- {misc[0]}: {misc[1]}")
# Summary of fermentation details
st.write(f"**Primary Fermentation:** {primary_fermentation_days} days at {fermentation_temp} °C")
if secondary_fermentation_days > 0:
    st.write(f"**Secondary Fermentation:** {secondary_fermentation_days} days")
if conditioning_days > 0:
    st.write(f"**Conditioning:** {conditioning_days} days")
# Summary of gravity and ABV
st.write(f"**Original Gravity:** {original_gravity}")
st.write(f"**Final Gravity:** {final_gravity}")
st.write(f"**Estimated ABV:** {abv:.2f}%")

# Closing message
st.markdown("""
**Happy Brewing!**
Keep notes for consistency and to improve your brewing process with each batch.
""")
