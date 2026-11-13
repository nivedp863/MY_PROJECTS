import streamlit as st


# ==========================================
# BUS PASS CLASS
# ==========================================

class BusPass:

    def __init__(self, passenger_name, age, source, destination, pass_type):

        self.passenger_name = passenger_name
        self.age = age
        self.source = source
        self.destination = destination
        self.pass_type = pass_type
        self.status = "Active"

        if pass_type == "Monthly":
            self.fee = 500

        elif pass_type == "Quarterly":
            self.fee = 1000

        elif pass_type == "Yearly":
            self.fee = 2000

        else:
            self.fee = 0

    def renew_pass(self):
        self.status = "Renewed"

    def cancel_pass(self):
        self.status = "Cancelled"


# ==========================================
# BUS PASS RESERVATION CLASS
# ==========================================

class BusPassReservation:

    def __init__(self):
        self.passes = []

    def reserve_pass(self, name, age, source, destination, pass_type):

        new_pass = BusPass(
            name,
            age,
            source,
            destination,
            pass_type
        )

        self.passes.append(new_pass)

        return new_pass


# ==========================================
# STREAMLIT CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Bus Pass Reservation",
    page_icon="🚌",
    layout="wide"
)


# ==========================================
# SESSION STATE
# ==========================================

if "system" not in st.session_state:

    st.session_state.system = BusPassReservation()


system = st.session_state.system


# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.title {
    font-size: 40px;
    font-weight: bold;
    color: #1f4e79;
}

.subtitle {
    font-size: 18px;
    color: #666666;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #dddddd;
    margin-bottom: 15px;
}

.card-title {
    font-size: 22px;
    font-weight: bold;
    color: #1f4e79;
}

.price {
    font-size: 24px;
    font-weight: bold;
    color: #008000;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="title">🚌 Bus Pass Reservation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Manage your bus passes easily and efficiently</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🚌 Bus Pass")

st.sidebar.write("Navigation")

page = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Reserve Bus Pass",
        "View Bus Passes",
        "Manage Pass"
    ]
)


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.header("📊 Dashboard")

    total = len(system.passes)

    active = 0
    renewed = 0
    cancelled = 0

    for bus_pass in system.passes:

        if bus_pass.status == "Active":
            active += 1

        elif bus_pass.status == "Renewed":
            renewed += 1

        elif bus_pass.status == "Cancelled":
            cancelled += 1


    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Passes",
            total
        )

    with col2:

        st.metric(
            "Active",
            active
        )

    with col3:

        st.metric(
            "Renewed",
            renewed
        )

    with col4:

        st.metric(
            "Cancelled",
            cancelled
        )


    st.divider()

    st.subheader("Recent Passes")

    if total == 0:

        st.info(
            "No bus passes available. "
            "Please reserve a bus pass."
        )

    else:

        for bus_pass in system.passes[::-1]:

            st.markdown(
                f"""
                <div class="card">

                <div class="card-title">
                🎫 {bus_pass.passenger_name}
                </div>

                <p>
                <b>Age:</b> {bus_pass.age}
                </p>

                <p>
                <b>Route:</b>
                {bus_pass.source} → {bus_pass.destination}
                </p>

                <p>
                <b>Pass Type:</b>
                {bus_pass.pass_type}
                </p>

                <p>
                <b>Status:</b>
                {bus_pass.status}
                </p>

                <div class="price">
                ₹{bus_pass.fee}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ==========================================
# RESERVE BUS PASS
# ==========================================

elif page == "Reserve Bus Pass":

    st.header("🎫 Reserve Bus Pass")

    st.write(
        "Enter the passenger details below."
    )

    with st.form("reserve_form"):

        name = st.text_input(
            "Passenger Name",
            placeholder="Enter passenger name"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=100,
            value=18
        )

        source = st.text_input(
            "Source",
            placeholder="Enter source"
        )

        destination = st.text_input(
            "Destination",
            placeholder="Enter destination"
        )

        pass_type = st.selectbox(
            "Pass Type",
            [
                "Monthly",
                "Quarterly",
                "Yearly"
            ]
        )

        if pass_type == "Monthly":

            st.info("Monthly Pass Fee: ₹500")

        elif pass_type == "Quarterly":

            st.info("Quarterly Pass Fee: ₹1000")

        else:

            st.info("Yearly Pass Fee: ₹2000")


        submit = st.form_submit_button(
            "🎫 Reserve Bus Pass"
        )


    if submit:

        if name.strip() == "":

            st.error("Please enter passenger name.")

        elif source.strip() == "":

            st.error("Please enter source.")

        elif destination.strip() == "":

            st.error("Please enter destination.")

        else:

            new_pass = system.reserve_pass(
                name.strip(),
                age,
                source.strip(),
                destination.strip(),
                pass_type
            )

            st.success(
                "Bus Pass Reserved Successfully!"
            )

            st.subheader("Pass Details")

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Passenger Name:**",
                    new_pass.passenger_name
                )

                st.write(
                    "**Age:**",
                    new_pass.age
                )

                st.write(
                    "**Source:**",
                    new_pass.source
                )

            with col2:

                st.write(
                    "**Destination:**",
                    new_pass.destination
                )

                st.write(
                    "**Pass Type:**",
                    new_pass.pass_type
                )

                st.write(
                    "**Status:**",
                    new_pass.status
                )

            st.success(
                f"Pass Fee: ₹{new_pass.fee}"
            )


# ==========================================
# VIEW BUS PASSES
# ==========================================

elif page == "View Bus Passes":

    st.header("📋 View Bus Passes")

    if len(system.passes) == 0:

        st.info("No bus passes available.")

    else:

        st.write(
            f"Total Passes: **{len(system.passes)}**"
        )

        for i, bus_pass in enumerate(system.passes):

            st.markdown("---")

            st.subheader(
                f"🎫 Pass {i + 1}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Passenger Name:**",
                    bus_pass.passenger_name
                )

                st.write(
                    "**Age:**",
                    bus_pass.age
                )

                st.write(
                    "**Source:**",
                    bus_pass.source
                )

                st.write(
                    "**Destination:**",
                    bus_pass.destination
                )

            with col2:

                st.write(
                    "**Pass Type:**",
                    bus_pass.pass_type
                )

                st.write(
                    "**Fee:**",
                    f"₹{bus_pass.fee}"
                )

                st.write(
                    "**Status:**",
                    bus_pass.status
                )


# ==========================================
# MANAGE PASS
# ==========================================

elif page == "Manage Pass":

    st.header("🔄 Manage Bus Pass")

    if len(system.passes) == 0:

        st.info(
            "No bus passes available."
        )

    else:

        # Create passenger names

        passenger_names = []

        for bus_pass in system.passes:

            passenger_names.append(
                bus_pass.passenger_name
            )


        selected_name = st.selectbox(
            "Select Passenger",
            passenger_names
        )


        # Find selected passenger

        selected_pass = None

        for bus_pass in system.passes:

            if bus_pass.passenger_name == selected_name:

                selected_pass = bus_pass
                break


        if selected_pass is not None:

            st.divider()

            st.subheader(
                f"🎫 {selected_pass.passenger_name}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Age:**",
                    selected_pass.age
                )

                st.write(
                    "**Source:**",
                    selected_pass.source
                )

                st.write(
                    "**Destination:**",
                    selected_pass.destination
                )

            with col2:

                st.write(
                    "**Pass Type:**",
                    selected_pass.pass_type
                )

                st.write(
                    "**Fee:**",
                    f"₹{selected_pass.fee}"
                )

                st.write(
                    "**Current Status:**",
                    selected_pass.status
                )


            st.divider()


            col1, col2 = st.columns(2)


            with col1:

                if st.button(
                    "🔄 Renew Pass",
                    use_container_width=True
                ):

                    if selected_pass.status == "Cancelled":

                        st.error(
                            "Cancelled pass cannot be renewed."
                        )

                    else:

                        selected_pass.renew_pass()

                        st.success(
                            "Bus Pass Renewed Successfully!"
                        )

                        st.rerun()


            with col2:

                if st.button(
                    "❌ Cancel Pass",
                    use_container_width=True
                ):

                    if selected_pass.status == "Cancelled":

                        st.warning(
                            "This pass is already cancelled."
                        )

                    else:

                        selected_pass.cancel_pass()

                        st.success(
                            "Bus Pass Cancelled Successfully!"
                        )

                        st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "🚌 Bus Pass Reservation System | "
    
)