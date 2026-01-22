
# Lecture 01: Big Issues in Mobile Information Systems
## Overview
Mobile Information Systems (MIS) differ from standard desktop computing due to specific constraints and contexts. The course highlights 7 key issues:
1. Limited Power
2. Limited Storage
3. Wireless Communication
4. I/O Capabilities
5. Unpredictable Context
6. Privacy & Security
7. Sustainability

---
## 1. Power Supply
The most critical constraint. Mobile devices are battery-dependent.

### The Trade-off
* **Capacity vs. Portability:** To get more power, you need a bigger battery, which increases size and weight.
* **Two Solutions:**
    1.  **Chemistry/Physics:** Increase energy density (hard, slow progress).
    2.  **CS/EE:** Decrease energy consumption (this is the focus of the course).

### Major Consumers
Ranked from highest to lowest consumption:
1.  **Display** (Backlight is the killer)
2.  **GPS & Camera**
3.  **Wireless Modules** (4G > 3G > WiFi > Bluetooth)
4.  **Sensors** (Accelerometer, etc.)

> [!TIP] Optimization Strategy
> Move computation-intensive tasks to the **Cloud** to save local battery, but balance this against the energy cost of data transmission.

### Energy vs. Data Transfer
* 4G consumes significantly more energy per KB than WiFi.
* **Tail Energy:** Wireless modules have a "tail" state where they stay high-power for a moment after transmission before sleeping.

---

## 2. Storage
Storage on mobile is limited (entry-level ~8-64GB) compared to desktop.
* **Technology:** Mobile uses **Flash Memory**.
* **Why Flash?** compared to Hard Disks (HDD):
    * **Density:** Flash ($\sim 1.5~GB/mm^3$) is much denser than HDD ($\sim 0.1~GB/mm^3$).
    * **Power:** Flash uses $\sim 0.1~W$ idle vs HDD $\sim 1~W$ idle.
    * **Durability:** No moving parts (shock resistant).
    * **Downside:** Price per TB is higher (~50€ vs ~15€ for HDD).

### The Cloud Trade-off
To solve storage limits, we "outsource" to the cloud.
* **Dependency:** Requires constant network connection.
* **New Trade-off:** Bandwidth usage vs. Local Storage space.

---

## 3. Wireless Communication
Wireless is the defining feature of MIS, but it is unreliable.
### Signal Theory Basics
* **Frequencies:** Generally 0.5 - 5 GHz (No Line-of-Sight required).
* **Channel Capacity** depends on:
    * **Bandwidth:** The range of frequencies used (e.g., 60 MHz).
    * **Modulation:** How data is encoded (AM/FM vs. Digital QAM).

### Transmission Regions
A signal isn't just "on" or "off". It has three zones:
1.  **Transmission Region:** Communication possible, low error.
2.  **Recognition Region:** Signal detected, but too weak to communicate.
3.  **Interference Region:** Signal adds to background noise, disrupting others.

### Physical Challenges (The Physics of Failure)
* **Refraction:** Waves bending through different densities.
* **Reflection:** Bouncing off smooth surfaces.
* **Absorption:** Energy absorbed by walls/water/bodies.
* **Diffraction:** Bending around small obstacles.
* **Interference:** Multiple transmitters on the same band (Crosstalk).
* **Multipath Scattering:** Signal taking multiple paths to the receiver (can be used as an advantage in [[MIMO]] systems).

### Antennas
* **Gain:** Efficiency of the antenna.
* **Radiation Pattern:** Real antennas are not perfect spheres (omnidirectional). They are dipoles or directional.
    * *Strategy:* Antenna selection can improve Signal-to-Noise Ratio (SNR).


### Network Classification
1.  **WLAN (Local):** 802.11 family (WiFi). Replacement for Ethernet.
2.  **WPAN (Personal):** Bluetooth, Zigbee. Short range (2-10m).
3.  **WWAN (Cellular):** GSM (2G), UMTS (3G), LTE (4G), 5G. Large coverage.

> [!NOTE] The ISM Band
> **Industrial, Scientific, and Medical (ISM)** bands (e.g., 2.4 GHz) are unlicensed. Your WiFi has to fight with microwave ovens, baby monitors, and industrial machines for this frequency space.

---

## 4. Input / Output (I/O)
Mobile devices have limited screen real estate and no physical keyboard.

### Touch Screen Issues
1.  **Occlusion:** Your hand covers the thing you are trying to touch.
2.  **Fat Finger Problem:** Fingers are low precision; they hit multiple pixels.
3.  **The Midas Touch:** There is no "hover" state. Every touch triggers an action immediately.

### Alternative Modalities
* **Gestures:** "Natural" but lack standards (is a swipe "delete" or "scroll"?). Hard to discover.
* **Speech:** Good for hands-free (car), but socially awkward and requires cloud processing (Siri/Google).
* **Motion:** Accelerometers/Gyros. Relative position only.
* **Vision:** Camera input (QR codes, AR). dependent on lighting.

---

## 5. Context
Context is more than just "Location."
### Types of Context
* **Environmental:** Light, Sound, Motion (Are you on a bus?).
* **Geometric:**
    * *Absolute:* GPS coordinates (Lat/Long).
    * *Relative:* Orientation, distance to other objects (6DOF).
* **Social:** Who is around? (Privacy, manners in a church vs. subway).
* **Activity:** What is the user *doing*? (Walking, sitting, taking a photo).

### The Recognition Problem
Automatic context detection is difficult.
* **False Positive:** Phone thinks you are in a meeting and blocks an emergency call.
* **False Negative:** Phone rings loudly during a funeral.

---

## 6. Security & Privacy
Mobile devices carry our most sensitive data (PINs, Location, Messages).

### The Risks
* **Data accumulation:** Apps, OS vendors (Google/Apple), and Gov agencies collect vast profiles.
* **Lack of Encryption:** Historically not pervasive (though improving).
* **Cloud Trust:** Offloading storage/processing requires trusting 3rd parties.

---

## 7. Sustainability
* **Carbon Footprint:** ~85kg $CO_2$ equivalent per phone (mostly manufacturing).
* **Lifecycle:** Short (~2 years).
    * *Hardware:* Battery degrades, screen breaks.
    * *Software:* **The main culprit.** Android vendors often stop security updates after 2-3 years, forcing obsolescence.
* **Solutions:** Right to Repair, Modular phones (FairPhone), LineageOS (community support).

---

## Review Questions
1. Why is **Flash memory** preferred over HDD for mobile, despite the higher cost?
	1. Flash memory unlike HDD has more space. It is in sense a very large place in a very small space. However the downside is the fact that its more expensive. It also uses less power which is a good way to make the phones more power efficient.
2. Explain the **"Tail Energy"** concept in wireless communication.
	1. When your mobile devise sends out high frequency signals it could be to communicate or send data, it often stays in a high power state even after sending the data. This even if only active for a second uses some extra power that could be saved.
3. What is the **"Midas Touch"** problem in UI design?
	1. The golden touch is the problem that for example unlike on a mouse as soon as you touch your screen an event is fired, this can be troublesome if you accidently hit you screen it fires an even. 
4. Differentiate between **Transmission**, **Recognition**, and **Interference** regions.
	1. Transmission: your phone is activilly resieving the signal possible to communicate
	2. Recognition: you know there is a signal but to weak to communicate
	3. Interference: signal to weak and adds to the background noise.
5. Why is **Context Recognition** risky for the user experience?
	1. Its important for the fact that context is important, how does your phone know if your driving, or taking a bus. Can it know that your in a meeting and then simply stop giving you notifications? 

## Exercise
![[HCI_Exercises.pdf]]
# Lecture 02: Location & Networks

## Part 1: Wireless Networks

### The Core Problem: Multiplexing
The RF spectrum is a shared, limited resource. To allow multiple devices to communicate without crashing into each other, we need **Multiple Access Methods** (Multiplexing).

#### 1. Time-Division Multiple Access (TDMA)
* **Concept:** Divide time into slots. Only one device speaks per slot.
* **Static:** Fixed timeslots. Requires precise clock synchronization.
* **Dynamic (CSMA/CA):** "Listen before you talk."
    * *Carrier Sense:* Check if the channel is idle.
    * *Collision Avoidance:* Use RTS/CTS (Request to Send / Clear to Send) to solve the **Hidden Node Problem** (where A can hear B, and C can hear B, but A and C cannot hear each other).

#### 2. Frequency-Division Multiple Access (FDMA)
* **Concept:** Divide the frequency band into smaller sub-channels.
* **Simple:** One frequency per user.
* **Complex (OFDMA):** Orthogonal Frequency-Division Multiple Access. Used in LTE/4G. Uses multiple sub-channels simultaneously.

#### 3. Code-Division Multiple Access (CDMA)
* **Concept:** Everyone speaks at once on the same frequency, but in different "languages" (codes).
* **Spread Spectrum:** The signal is spread over a wider bandwidth than necessary.
    * *FHSS (Frequency Hopping):* Rapidly switching frequencies in a pseudo-random sequence (used in Bluetooth).
    * *DSSS (Direct Sequence):* Data is multiplied by a high-rate bit sequence (used in old WiFi and 3G).


---

### Wireless Standards Families

#### 1. Bluetooth (WPAN)
* **Range:** Personal Area Network (2-10m).
* **Complexity:** Massive specification (>3000 pages). Covers all protocol layers.
* **Air Interface:** 2.4 GHz ISM band. Uses **FHSS** (Adaptive Frequency Hopping) to avoid interference.
* **Two Flavors:**
    1.  *Classic:* Headsets, keyboards.
    2.  *Low Energy (BLE):* Sensors, wearables, IoT.

#### 2. WiFi (WLAN)
* **Standard:** 802.11x family.
* **Scope:** Covers only the bottom 2 layers of the OSI model (Physical & Data Link).
* **Topology:** Usually Star (Access Points), but supports Ad-hoc/Direct.
* **Interference:** Shares 2.4 GHz with Bluetooth. Modern devices use coexistence strategies (time-sharing the antenna).

#### 3. Cellular (WWAN)
* **1G:** Analog (FDMA).
* **2G (GSM):** Digital (TDMA). ~200 kBit.
* **3G (UMTS):** CDMA. ~20 MBit. Hybrid of Circuit-Switched (Voice) and Packet-Switched (Data).
* **4G (LTE):** OFDMA. ~300 MBit. Purely IP-based (Packet-switched only). Voice is now VoIP.
* **5G:** Higher speeds (~2 GBit), microcells, IoT support, Car-2-Car communication.

> [!INFO] The Black Box Problem
> In cellular devices, the "Baseband" processor runs a proprietary, closed-source OS that handles all radio communication. It is separate from the main OS (Android/iOS) and represents a significant security/privacy black hole.

---

## Part 2: Location

### Location Classes
1.  **Geographic:** Latitude/Longitude (e.g., N 50.97, W 11.32).
2.  **Topological:** Street address (e.g., "Karl-Haußknecht-Str. 7").
3.  **Cell-based:** ID of the current network cell (WiFi MAC or Cell Tower ID).

> [!TIP] Mapping
> * **Geocoding:** Address $\to$ Coordinates.
> * **Reverse Geocoding:** Coordinates $\to$ Address.

### Location Determination Methods

| Method | Pro | Contra | Accuracy |
| :--- | :--- | :--- | :--- |
| **Satellites (GPS)** | High Accuracy | High Power, Needs Line-of-Sight (Outdoor only) | ~1 m |
| **WLAN Cells** | Low Power | Medium Accuracy, Database dependent | ~10-100 m |
| **Cell Towers** | Zero extra power | Low Accuracy | ~100-1000 m |

### GPS (Global Positioning System)
* **Mechanism:** Time-of-Flight (TOF). The receiver measures how long signals take to arrive from satellites.
* **Math:** Triangulation (technically Trilateration).
    * 3 Satellites = Intersection of 3 spheres (2 points, one is in space, one is on Earth).
    * **4th Satellite:** Required to correct the receiver's imprecise clock (Time Difference of Arrival - TDOA).
* **Constellation:** ~32 satellites at ~20,000 km altitude.
* **Extensions:**
    * *A-GPS (Assisted):* Downloads orbital data (Almanac) via internet to speed up the "First Fix."
    * *D-GPS (Differential):* Uses ground stations to correct errors.

> [!WARNING] The China Problem
> Most of the world uses **WGS-84** coordinates. China uses **GCJ-02**, which intentionally adds random offsets to coordinates for national security. Using standard GPS data on a Chinese map results in a mismatch.

### Cell-Based Location
* **How it works:** Look up the unique ID of the WiFi Router (MAC address) or Cell Tower in a massive database to get its known location.
* **Issues:**
    * *Dynamic:* WiFi routers move (people move houses).
    * *Privacy:* Queries are logged by providers (Google/Mozilla/Apple).
    * *Offline:* Cannot work without an internet connection to query the DB (unless the DB is downloaded, which is huge).

---

## Review Questions
1. What is the **Hidden Node Problem** in wireless networking, and how does **RTS/CTS** solve it?
	1. The hidden node problem 
2. Explain the difference between **FHSS** (Bluetooth) and **DSSS** (WiFi).
	1. Frequency hopping switches between multiple different pseudo random frequiices in a rapid fashion 
	2. Direct sequences multiplies a frequency by a bitstring
3. Why does GPS require **4 satellites** for a fix instead of just 3?
	1. we need the 4th satelite to correct the recievers imprecise clock TDOA time tifference of arriaval
4. What is the difference between **Geocoding** and **Reverse Geocoding**?
	1. Geocoding you go from an adress to coodinates reverse does the opposite.
5. Why is **Cell-based location** preferred over GPS for indoor applications?
	1. Sattelites require a direct LOS (Line of sight) whereas cells use overlapping cells, each cell has a different frequency you can therefor see where you overlap. 
# Lecture 03: I/O on Small Screens

## 1. Input Challenges (Recap)

Mobile interaction is primarily constrained by the physical size of the device and the nature of human-computer interaction in mobile contexts.

- **Haptic Feedback**: Unlike physical keyboards, touchscreens lack tactile confirmation.
- **Occlusion**: The user's hand or fingers naturally cover parts of the display during interaction.
- **Precision**: The "fat finger problem" refers to the fact that a finger covers a target and hits multiple pixels simultaneously.
- **Midas Touch**: The lack of a "hover" state means every touch immediately triggers an action.
- **Reachability**: Screen sizes have grown beyond the natural comfortable "Thumb Zone" for one-handed use.

---

## 2. Touch Interaction Solutions

### Haptic Feedback
- **Physical Overlays**: Technologies like "Phorm" use microfluidics to create physical buttons that "grow" out of the screen.
- **Vibration**: Standard vibration alerts provide a binary or patterned channel for confirmation.
### Precision & Occlusion
- **Offset Cursors**: Showing a cursor slightly above the finger to avoid occlusion.
- **Handles & Menus**: Using specific handles for selection or menus that appear offset from the touch point.
### The Midas Touch Problem
- **Activation on Lift**: A common solution is to wait to trigger the action until the finger is lifted off the screen, allowing the user to adjust their aim.

---

## 3. Input Modalities

### Gestures
- **Discrete Gestures**: Tap, double tap, long press, swipe.
- **Continuous Gestures**: Pinch-to-zoom (one of the few standardized gestures).
- **Bezel Swipes**: Starting a gesture from the black frame of the device to trigger system-level actions (e.g., Back, Notification shade).
- **Discoverability**: A major issue with gestures is that users often do not know which gestures are available.
### Motion & Sensors
- **Accelerometer/IMU**: Used for orientation switching (Portrait vs. Landscape), shaking to undo, or tilting for navigation.
- **Vision (Camera)**: Used for barcode/QR code scanning, face tracking, and 3D reconstruction (SLAM).

### Speech
- **Speech Input**: Primarily used for hands-free scenarios like car navigation or simple assistants (Siri, Google).
- **Offloading**: Complex recognition is usually offloaded to a cloud service.
---

## 4. Output Modalities

### Audio Output
- **Earcons**: Abstract musical patterns that require learning (e.g., a specific "ding" for a new email).
- **Auditory Icons**: Natural, metaphorical sounds that are immediately intuitive (e.g., the sound of a trash can for deleting a file).

### Display Technology
- **LCD (Liquid Crystal Display)**: Requires a backlight; consumes power regardless of color displayed.
- **OLED (Organic Light Emitting Diode)**: Each pixel is self-illuminating; black pixels are "off," which saves power.
- **E-Ink (Electronic Paper)**: Bistable (consumes power only when the image changes) and highly readable in sunlight, but has very slow refresh rates.
### Display Quality & Resolution
- **PPI (Pixels Per Inch)**: Higher PPI is needed for handheld devices compared to TVs because they are held closer.
- **PenTile Matrix**: A subpixel layout used in some OLED displays that shares subpixels to increase density but can result in "fuzzy" text or color fringes.

---
## 5. Text Entry Strategies
- **Multi-tap**: Pressing a key multiple times for different letters (e.g., 2 for 'a', 22 for 'b').
- **Predictive Text (T9)**: Using a dictionary to disambiguate single key presses.
- **Shape Writing/Swyping**: Drawing a continuous path through letters to form words.

---
## Review Checklist
1. Explain the **"Midas Touch Problem"** and how lift-off activation solves it.
	1. The midas touch problem is the problem that when you touch  the screen an event fires you can sort of solve this by waiting for the user to lift their fingers off the screen before firing the event
2. Differentiate between **Earcons** and **Auditory Icons**.
	1. Earcons have to be learned while auditory is something we assosiate with the given thing being heard
3. Why is **OLED** more energy-efficient for dark-themed apps?
	1. Because OLED has its black pixels off unless needed unlike LED where everything is turned on at the same time
4. What is the impact of **occlusion** on mobile UI design?
	1. Occlusion is a big deal in UI design you have to be able to design a UI that is still intuative while some of it is hidden by the thumb or other fingers.

## Presentation Notes: The "Throw App"
### 1. Project Overview
- **Goal:** Create an application that measures how high a user throws their phone into the air.
- **Core Technology:** Uses the device's **Accelerometer** sensor to detect "Free Fall."
- **Key Concept:** Utilizing implicit input (motion) rather than explicit input (touch/buttons)
### 2. The Physical Principle (The "Why")
- **Resting State:** When the phone is in your hand or on a table, the accelerometer measures **1g (approx 9.8 $m/s^2$)** due to Earth's gravity pushing against it.
- **Free Fall State:** When an object is thrown or dropped, it enters "micro-gravity." The accelerometer readings for x, y, and z will all drop close to **0**.
- **Detection Strategy:** We monitor the sensor stream. When the total G-force drops near zero, we know the throw has started. When it spikes back up, the phone has been caught.
### 3. Implementation Details

#### A. Sensor Fusion (Magnitude)
- **Code:** `double gForce = sqrt(event.x^2 + event.y^2 + event.z^2);`
- **Explanation:** We cannot just look at the Y-axis because the phone spins while flying. We calculate the **Magnitude** of the force vector. This ensures the app works regardless of the phone's orientation.
#### B. The State Machine
My code implements a simple 3-state logic:
1. **Ready:** Monitoring sensor. G-Force is normal (~9.8).
2. **In Air (Free Fall):** Triggered when `gForce < 2.0`.
    - _Action:_ Start a stopwatch (`DateTime.now()`).
    - _Visual Feedback:_ Background turns Blue.
3. **Caught:** Triggered when `gForce > 2.0` (Impact).
    - _Action:_ Stop stopwatch. Calculate height.
#### C. Filtering Noise (Signal Processing)
- **Thresholding:** I used a threshold of `2.0` rather than `0.0` to account for sensor noise and minor air resistance.
- **Time Filter:** `if (flightTimeMs > 200)`
    - _Reason:_ Hand tremors or putting the phone on a table quickly might look like free fall for 10-50ms. I filter out any "throws" shorter than 0.2 seconds to prevent false positives.
        
### 4. The Physics Calculation

Once we have the **Total Flight Time**, I calculate the height:
1. **Assumption:** The throw is symmetric (Time Up = Time Down).
2. **Time to Apex:** $t = \text{TotalTime} / 2$.
3. **Formula:** $h = \frac{1}{2} g t^2$
    - $g = 9.81$
    - This gives us the peak height in meters.
### 5. Challenges & Limitations
- **Centripetal Force:** If the phone spins violently while thrown, the accelerometer might measure the spin force (centripetal) instead of pure gravity. This could prevent the reading from dropping below 2.0, causing the app to "miss" the throw.
- **Soft Catches:** If the user catches the phone very gently (decelerating slowly), the G-force might not spike immediately, leading to inaccurate timing.
- **Safety:** I added `SystemChrome.setPreferredOrientations` to lock the screen in Portrait mode. Allowing rotation during a throw makes the UI unreadable and jittery.
### 6. Demo
_(Show the app)_
- **Black Screen:** Ready.
- **Blue Screen:** In Air (Instant feedback).
- **Green Screen + Result:** Caught (Shows height).

---
# Lecture 04: UbiComp & IoT
## 1. Ubiquitous Computing (UbiComp)

**Core idea (Weiser, 1991):**
- The most powerful technologies “disappear” into everyday life.
- The goal is computing that feels _embedded_ and _natural_, not something you constantly “operate.”

**Weiser’s 3 device classes:**
- **Tabs**: wearable, centimeter-scale devices
- **Pads**: handheld, decimeter-scale devices
- **Boards**: meter-scale interactive displays  
    → The lecture’s point: a lot of this vision has “mostly arrived” in hardware form.

**But… has it really arrived?**
- UbiComp isn’t only about _devices_ — it’s also about _interaction (or lack of interaction)_.
- Related terms: **calm / ambient / pervasive computing**
    - Implies _less manual setup_ and less “user effort.”
- Practical example problem: even pairing/using multiple Bluetooth devices smoothly is still hard.
---
## 2. “Internet of Things” (IoT)
**Framing:**
- Often used as a broad marketing term.
- Still, the core concept is clear: **connectivity everywhere**.

**How IoT differs slightly from classic UbiComp:**
- Less focus on personal interactive devices.
- More focus on **smart objects + sensor networks**
    - Examples: light bulbs, fridges, trash cans, water meters
- Also overlaps with industrial visions like **Industry 4.0 / Factory of the Future**.

**Stated goals:**
- Automate mundane everyday tasks
- Improve energy/resource efficiency
- “Smarter” logistics (especially factories)

**Less idealistic goals (implied):**
- Sell more sensor/wireless modules
- Collect more consumer data (sometimes surprisingly informative)
---
## 3. Big Issues in UbiComp/IoT

### Energy / Power Supply
- Scaling problem: imagine replacing batteries in **thousands** of devices.
- Leads to interest in **energy harvesting** (see section 7).
### Interaction & Usability
- People already struggle managing **two** devices.
- Question becomes: how do you manage **huge networks** of devices with minimal setup?
### Privacy & Security
- Massive amounts of personal and environmental data.
- Needs strong protection — but IoT often ships with weak defaults.
### Standards (or lack thereof)
- Interoperability is a mess: different vendors, different protocols, different apps.
- Results in “Device A can’t talk to App B” problems.
---
## 4. UbiComp/IoT Technology Landscape

The lecture groups the enabling tech into:
- **Wearables & interaction concepts**
- **Sensor & mesh networks**
- **Personal area networks** (e.g., BLE, NFC)
---
## 5. Wearables & Interaction Concepts
**Wearable = body-worn, hands-free device**, e.g.:
- Smartwatches, fitness trackers
- Smart glasses (e.g., Google Glass)
- Headsets/headphones (borderline but often included)

**Why interaction is special here:**
- Very small screens (or no screen)
- New input styles:
    - simple swipes
    - shake/motion gestures
    - voice commands
### Smartwatches (high-level notes)
**Why they became popular recently:**
- They act as a **companion** to the smartphone (less heavy lifting on the watch)
- Better sensors (motion, heart rate, etc.)
- Better displays

**Typical problems:**
- Battery lifetime
- Physical size constraints

**Interaction style:**
- Rough swipes / motion gestures (not “full smartphone gesture sets”)
- Often tightly coupled to phone interaction (notifications, quick replies)

**Common use cases:**
- Notifications + short actions
- Body/activity/sleep logging
- “Quick glance” information
---

## 6. Sensor Networks, Mesh Networks, and LPWAN

### Why “regular” network topologies struggle
- Classic star/tree networks rely on **central hubs**.
- IoT sensors are often:
    - **low power**
    - **short range**
- So you’d need lots of hubs/gateways → expensive and annoying.
### Mesh networks (the alternative)
- Every device can act as a **relay/hub**.
- Data may travel across multiple **hops**.
- Network topology can change dynamically.

**Forwarding strategies mentioned:**
- **Flooding / rebroadcasting** (simple but can cause overhead)
- **On-demand routing** (example: AODV)
- **Pro-active routing** (examples: OLSR, B.A.T.M.A.N.; community networks like Freifunk)

**Implementations mentioned:**
- ZigBee (IEEE 802.15.4)
- Bluetooth LE mesh (newer versions)
- WiFi-based community meshes
### LPWAN (Low Power Wide Area Networks)
- Long range (roughly kilometers)
- Very low bandwidth (good for tiny sensor updates)
- Examples mentioned: LoRaWAN, Weightless, WiFi HaLow
- Intended for things like smart meters and street lamps
---
## 7. Personal Area Networks (WPAN): Bluetooth → BLE → NFC

### “Classic” WPAN idea
- Goal: connect personal peripherals.
- Historically: IrDA → Bluetooth.

**Classic Bluetooth drawbacks (in this lecture’s framing):**
- Higher power draw
- Pairing/setup complexity
### Bluetooth Low Energy (BLE / BTLE)
**Key idea:** optimized for small battery sensors that should last months/years.
**BLE characteristics:**
- Same 2.4 GHz ISM band as classic Bluetooth
- Smaller / less complex stack
- Introduced in Bluetooth 4.0
- Max data rate around 1 Mbit/s (lecture-level takeaway: not for heavy streaming)

**Two roles:**
- **Peripheral**
    - broadcasts or connects to one central
    - can notify central on value changes
- **Central**
    - scans, connects, receives notifications

**Device “complexity classes” (practical categories):**
- **Beacons**: static broadcasts (e.g., iBeacon UUID)
- **Sensors**: broadcast/unicast sensor data; notification support reduces polling
- **Bidirectional**: mostly for configuration/parameters rather than synchronous chat

**Power concept to remember:**
- Advertising interval heavily affects lifetime.
- Power management is a core design constraint.
### BLE protocol structure (names to recognize)
- **GAP (Generic Access Profile)**  
    Advertising, discovery, connection setup; small broadcast payload (+ optional extra on request).
- **GATT (Generic Attribute Profile)**  
    The main structure for “live” data: services + characteristics identified by UUIDs, publish/subscribe style, supports notifications.
### Near Field Communication (NFC)
**NFC basics:**
- Very cheap tags, many physical form factors.
- Subclass of RFID.
- Passive tags are powered by the reader’s magnetic field.
- Communication is short-range and based on field modulation.

**Typical NFC characteristics:**
- Very short range (centimeters)
- Storage from tiny to moderate (think: “IDs/URLs up to small data blocks”)

**Variants / types:**
- Simple storage (NDEF-style use)
- Smart cards with crypto (e.g., Mifare-like concept)
- Java cards (programmable)
- Card emulation (phone pretends to be a card)

**Use cases:**
- URLs/contact data in posters/business cards
- Access control / student cards
- Mobile payment
- Passports (sensitive data)
- Device-to-device sharing (historically, e.g., Android Beam)

**Security notes:**
- Public tags ideally should be write-protected (often they aren’t)
- Risks include tag rewriting (e.g., malicious URLs)
- Low-level protections (keys) can be attacked in practice
- Higher-level: dedicated crypto apps in the chip (SIM-like security model)
---
## 8. Major IoT Problem Deep Dives

### Energy supply → Energy harvesting

Possible sources mentioned:
- Light (sun/environment)
- Vibration & sound
- Temperature differences
- Ambient EM radiation

Tradeoffs:
- Low efficiency (tiny power budgets)
- Need storage (e.g., night time)
### Privacy
- BLE broadcasting can enable tracking.
- Extra data leakage risk (e.g., broadcasting sensor data like pulse).
- MAC randomization exists, but isn’t always used.
- Classic tradeoff: **security/privacy vs ease of setup**
- Real-world stalking risk examples: item trackers.
### Security
- Phones are already patch-challenged; IoT devices are often worse.
- Many devices remain unpatched because users don’t notice or vendors don’t support them long.
- Insecure IoT can become part of botnets and be used for attacks (e.g., DDoS).
### Standards
- Often “one standard per manufacturer.”
- Sometimes common ground is IP; more recently, cross-vendor efforts exist (lecture mentions Matter).
- Reality: a mix of protocols (HTTP, MQTT, ZigBee, etc.)
- “Universal” approach idea: devices broadcast a URL (Physical Web / URIBeacon concept)
    - Challenge: mapping the URL to the right meaning/control model.
---

## Review Checklist
1. Explain UbiComp in Weiser’s sense: what does it mean for technology to “disappear” into everyday life?
2. Tabs vs Pads vs Boards: give an example of each in modern terms.
3. Why do mesh networks help IoT deployments compared to star/tree networks?
4. BLE roles: what’s the difference between a central and a peripheral?
5. What are GAP and GATT used for (at a high level)?
6. Give two NFC use cases and one NFC security risk.
7. Name the four big IoT issues highlighted: energy, interaction, privacy/security, and standards.
## Presentation Notes: "Emoji Broadcast" (Wear OS)
### 1. Project Overview
- **Goal:** Create a localized, "serverless" chat application for Smartwatches.
- **Core Technology:** Bluetooth Low Energy (BLE).
- **Concept:** Instead of pairing devices or connecting to the internet, we use **BLE Advertising** to "shout" messages to anyone nearby and **BLE Scanning** to hear them.
- **Use Case:** Proximity-based social interaction (e.g., sharing a mood in a classroom or club) without exchanging contact info.
### 2. The Protocol: "Connectionless" Communication

Standard Bluetooth involves pairing and bonding. We skipped that to make the interaction instant and fluid.
- **Broadcaster Role (Peripheral):** To send a message, the watch turns into a beacon.
    - _The Hack:_ We are embedding the message directly into the **Device Name** field of the advertisement packet.
    - _Format:_ `sHCI:[Your_Emoji]` (e.g., `sHCI:😎`).
- **Observer Role (Central):** To receive messages, the watch scans for _any_ advertising packets in the air.
    - _Filtering:_ We ignore standard devices (Headphones, Fitbits) and only look for names starting with `"sHCI:"`.
### 3. Implementation Details
#### A. Permissions (The Gatekeeper)
- **Android 12+ Requirements:** The code explicitly requests `BluetoothScan`, `BluetoothConnect`, and `BluetoothAdvertise`.
- **Location:** We also ask for `Location` because, historically on Android, scanning for Bluetooth devices could be used to derive a user's physical location.
#### B. The Scanning Logic (Listening)
- **Stream:** We listen to `_centralManager.discovered`.
- **Deduplication:**
    - _Problem:_ BLE devices send advertisements ~3 times per second. We don't want the list to flicker or fill up with duplicates.
    - _Solution:_ I used a `Map<String, String>` where the key is the sender's **UUID** (Unique ID). I only update the UI if the message content associated with that UUID changes.

#### C. The Advertising Logic (Talking)
- **Action:** When you type an emoji and hit send:
    1. We construct the name: `"sHCI:" + text`.
    2. **Important Step:** We strictly `stopAdvertising()` before `startAdvertising()`.
    3. _Why?_ You cannot change the name of a live advertisement dynamically. You must tear down the old broadcast and erect a new one with the new payload.

### 4. Wear OS Specifics (UI/UX)
Developing for a watch is different from a phone:
- **OLED Optimization:** The `backgroundColor` is set to `Colors.black`. On OLED watch screens, black pixels are off, which saves massive amounts of battery.
- **Round Layout:** I used a `Center` widget with `Padding` to ensure content isn't clipped by the rounded corners of the watch face.
- **Input Constraint:** Typing on a watch is hard. I set `TextInputAction.send` so the user can broadcast directly from the keyboard's action button, keeping interaction quick.
### 5. Challenges
- **Payload Limit:** The BLE Advertisement packet is tiny (31 bytes). The Device Name consumes most of this. This is why we restricted it to **Emojis** or very short words—long sentences would get truncated or dropped.
- **Latency:** BLE scanning is power-constrained. It might take 1-3 seconds for a friend's new emoji to appear depending on the scan interval.
### 6. Demo Flow
1. **Scanning State:** App opens, shows "Scanning..." (Central Mode active).
2. **Broadcasting:** I type "🔥". The app starts advertising `sHCI:🔥`.
3. **Discovery:** Another watch nearby picks up the packet, strips the `sHCI:` prefix, and adds "🔥" to the feed.

# Lecture 05: Mixed Reality

## 1. Where AR fits: the Virtuality Continuum
- **Augmented Reality (AR)** is part of the **“Virtuality Continuum”** (Milgram & Kishino, 1994).
- AR is a **subclass of Mixed Reality (MR)**.
- AR can be **roughly categorized by the ratio** between real and virtual content.
---
## 2. Definition of AR (Azuma, 1997)
AR characteristics:
- Mix of **real-world + virtual visual information**
- **Interactive in real-time**
- **Real and virtual elements are spatially aligned in 3D**

Requirements (from the slides):
- Visual input (real world) + visual output (virtual)
- User input + fast graphics (to enable interaction)
- **6D head tracking** (for spatial alignment)
---
## 3. AR history & pioneers (high-level timeline)
- **1901**: first mention of the idea in a novel (“The Master Key” by L. Frank Baum)
- **1968**: first head-mounted display (HMD) (“The Sword of Damocles” by Ivan Sutherland)
- **1980**: first wearable HMD by Steve Mann
---

## 4. AR head-mounted displays (HMDs)

### Optical see-through HMD
How it works:
- Uses a **beam combiner** + focus optics to overlay display image over the real-world view.
Pros:
- Direct view of the real world
- Eye can focus at different distances
Cons:
- (Mostly) cannot “cover” real objects (3D occlusion problem)
- Lag/alignment issues are more obvious
### Video see-through HMD
How it works:
- Similar to VR displays + **camera** (video mixing).
Pros:
- Camera image can be used for tracking → less lag, better alignment real ↔ virtual
- Real objects can be hidden/substituted
Cons:
- **Parallax error** (camera ↔ display)
- Similar problems to VR displays (motion sickness)
- Single focus distance
---
## 5. Commercial HMD examples mentioned
Optical see-through:
- Google Glass, Meta Wayfarer (**not AR!**)
- Microsoft Hololens
- Magic Leap
Video see-through:
- Smartphone goggles (Google Cardboard, Samsung Gear VR)
- Meta Quest 3, Lenovo Mirage Solo
- VR headset + add-on cameras
---
## 6. Practical issues with HMDs
General HMD issues:
- Brightness (especially outdoors/sunlight)
- Field of view (FOV): human FOV ~180°, many HMDs only ~20°
- Weight/comfort (can induce headaches)
- Lag between:
    - real and virtual content
    - head and image movement
- Safety concern: what if video see-through fails while crossing the street?
Issues with Cardboard & similar:
- Only a single camera on most devices → no 3D view for AR possible (“flat screen effect”)
- (Mostly) no positional tracking, only rotation → higher probability of motion sickness
- Unpredictable device capabilities
- Uncomfortable weight distribution
- Touchscreen inaccessible
---
## 7. HUDs and “diminished” reality
### Heads-up displays (HUDs)
- Mostly used in vehicles (car, airplane)
- Shows navigation info, speed, horizon, etc.
- Not always spatially aligned
- Uses beam combiner (windshield) + 2D display
### Augmented Diminished Reality (idea/example)
- Not adding, but **removing** real-world content?
- Example given: **HDR welding mask/goggles**
    - Filters out welding arc    
    - Other details remain visible    
---
## 8. Mobile devices as AR displays
- Uses a “**window into virtual world**” metaphor
- Usually no 3D display
    - Except with tricks like Google Cardboard
    - Parallax issues  
- Primary problem highlighted: **location/tracking**
---
## 9. AR tracking & localization (core requirement)
- Fundamental requirement: stable & reliable **head/view tracking**
- Multiple approaches:
    - **GPS + IMU**
    - **Vision-based**
    - Stereo/depth cameras
    - SLAM algorithms
### GPS + IMU
- Sensor fusion for **6D pose (geo coordinates)**
    - 3D position from GPS, 3D orientation from IMU 
    - (Relatively) low accuracy & position
    - Requires additional environment information
- Best suited for large-scale applications (e.g., buildings)
- Examples: Pokemon Go, Layar, Wikitude Browser
### Vision-based tracking (overview)
Primary goal: retrieve **6D pose**  
Secondary goal: create environment map → enables interaction with environment
Two paths mentioned:
- With specialized hardware:
    - Add-on stereo cameras / depth cameras
    - iPad Pro (tablet with depth cam)
- On arbitrary devices (single RGB camera):
    - Marker-based (fiducial/image)
    - SLAM algorithms
### Stereo/depth cameras
- Core idea: each pixel provides color + distance
- Stereo cameras:
    - 2 cameras in parallel
    - Find stereo correspondences between 2 images
    - Use camera/lens geometry to calculate distance
- Depth cameras (single camera + emitter):
    - ToF (time-of-flight): measure travel time of IR flash
    - Structured light: shift in projected light pattern
- Both require specialized hardware
### Marker-based tracking
- Use pre-defined markers/targets:
    - **Fiducials**: printed black-and-white patterns
    - **Image targets**: (flat) real-world objects
- System detects pose relative to target
Marker-based + SIFT:
- **SIFT** = Scale Invariant Feature Transform
    - Detects key points in images
    - Describes them independent of size, rotation, …
    - Descriptors can be matched across images → calculate geometric transformation
### SLAM
- **Simultaneous Localisation & Mapping**
    - Creates 3D environment map + 6D camera pose
    - Requires only a single camera
    - Works on almost any device
    - Creates stereo correspondences from motion
    - (Optionally) uses IMU data to determine motion magnitude

Practical notes from the slides:
- Map generation requires significant processing power
- Possible on most recent smartphones with ARKit/ARCore frameworks
- Needs calibration data for camera (distortion) + IMU (alignment to camera)
- Includes plane detection (floor, tables, walls) for object placement + shadows
- Touchscreen-based interaction

---
## 10. Spatial AR / Projection Mapping
- Projects augmentations directly onto the real world
- Mostly static projector/camera setups
    - e.g., buildings, cars, other large objects
    - pico projectors for mobile use (mentioned as a question/idea)
- Big problem: brightness vs power supply
- Other issue: focus distance (laser projectors)
- Requires:
    - accurate environment maps
    - object tracking
Industrial usage example:
- Project assembly instructions onto a workpiece (“Werklicht” by Extend3D)
    - Needs high brightness & focal depth (laser projector required)
    - Workpiece geometry needs to be known in advance → target for visual tracking (similar to image targets)
---
## 11. Interaction with AR (methods listed)
- Touch screen (e.g., “Touch Projector”, AI Pin)
- Individually tracked tools (e.g., Wiimote, gloves)
- Optical recognition/tracking of hands

---
## 12. AR applications (examples listed)
- AR still waiting for the “killer app”
- Advertisements (Ikea, fashion)
- Military: cockpits, weapon sights
- Education (e.g., iSkull)
- Repair & maintenance
- Gaming (e.g., Ingress, Pokemon Go)
- Medical applications (“X-ray vision”)
- Navigation (only prototypes)
---

## 13. “Mobile” Virtual Reality (as covered here)
- Meta Quest 1–3: no cables (mobile HW)
- 4 low-res high-speed IR cameras
    - tracking of hands/controllers
    - “room-scale” 6DoF tracking
- No obstacle detection, only pre-defined safety boundaries → needs large space
- Possible workaround: “redirected walking”
- General research topic in VR: locomotion
---

## Review Checklist
1. What are the **three AR characteristics** in Azuma’s definition?
2. Compare **optical see-through** vs **video see-through** HMDs: one pro + one con each.
3. List the **main issues with HMDs** (brightness, FOV, weight, lag, safety).
4. Why is **location/tracking** the primary problem for mobile AR displays?
5. Name and describe the tracking approaches: **GPS+IMU**, **marker-based**, **stereo/depth**, **SLAM**.
6. What does **SLAM** produce, and what extra features do ARKit/ARCore-style systems include (per the slides)?
7. What does **projection mapping** require, and what is the “Werklicht” use case?
# lecture: 06 - Case Studies
## 1. Inside the Amazon Dash Button
### What it is
* A **prototypical IoT device**
* A **single physical button** for ordering **one specific product** 
### What’s inside (hardware highlights)
* **Microcontroller** (reprogrammable)
* **Board antenna**
* **WiFi module**
* **Button**
* **Microphone** (“why?”)
* **Battery** (non-rechargeable) 
### The “chicken-and-egg” IoT setup problem

Problem:
* Needs **WiFi configuration**, but has **no normal UI**
  → How do you enter network + password? 
Solutions shown:
* **Approach 1: Temporary local hotspot (Android style)**
  * Dash creates its own hotspot
  * Phone connects and sends WiFi credentials
  * Dash closes hotspot, connects as a WiFi client 
* **Approach 2: Side-channel configuration (iOS style)**
  * iOS app sends config via **ultrasound**
  * Dash listens for sound patterns and extracts config 
* **Approach 3 (mentioned):** misuse of WiFi layer-2 frames (“ProbMe”) 

---
## 2. Tweaks without root access

### Netguard: user-level network filtering
* Android blocks **root-level** access to network (unless rooted)
* **Loophole:** VPN apps are allowed at user level
* Can be (ab-)used for **network filtering**
* Useful for blocking **ads/trackers** 
### PixOff: AMOLED battery saver
* Selectively turns off **individual pixels**
* **Doesn’t work for LCD** screens (prompted as “why?”)
* Different visual patterns depending on user preference
* “Currently not available in Play Store?” (as noted on slide) 
### Secondary uses for old devices
* **Kiosk mode apps**
  * Lock device to a single app (music player, web browser)
  * Useful for creating “appliances”
* **Room surveillance**
  * Use camera, microphone, IMU to watch for intruders
  * Example listed: **Haven (open-source)** 
### Macro / automation tools

* Examples: **MacroDroid**, **Automate**
* Sometimes close to a full development environment
* Potential usability issues
* Risk example: accidentally lock yourself out of your own device 

---
## 3. COVID-19 Contact Tracing (cartoon walk-through)

Core mechanism shown:
* Phones broadcast **random messages** every few minutes
* Nearby phones **exchange** those messages
* Both phones remember what they “said” and “heard” over the past **14 days** 
If someone becomes a case:
* They send their messages to a hospital/system
* Because messages are random, **no personal info is revealed** to the hospital 
Exposure notification:
* Your phone can check whether it “heard” any messages from COVID-19 cases
* If it heard **enough** messages (exposed long enough), you get alerted 

---
## 4. Apple AirTags & “Find My”

### Standard process (BLE + public-key crypto)
* Initial setup creates a **public/private keypair**
* AirTag **broadcasts the public key** (BLE)
* Other devices upload their own location, **encrypted with the public key**
* Owner uses the **private key** to download + decrypt the GPS location 
### Extra technologies and capabilities
* iPhone 11+: **Ultra Wide Band (UWB)** for “last-meter” localization
* Android devices can use **NFC** to identify an AirTag on contact 
### 3 wireless technologies in one device (as listed)
* **BTLE**: broadcasting public key (and audio notifications)
* **NFC**: direct-touch identification & pairing
* **UWB**: last-meter localization 
### Issues noted
* Not a large issue: **owner privacy** (due to public-key crypto)
* Big issue: **stalking & theft**
* iPhones try to detect unknown AirTags moving with you
* Android needs a custom app 

---
## 5. Mobile Card Emulation

### Two modes
* **Host Card Emulation (HCE)** (top)
  * Less secure: malware can interfere with payment process
* **Secure Element Mode (SEM)** (bottom)
  * Harder to implement: requires extra security chip (e.g., Apple Pay)
* Google Pay: issues with carrier support (restricted SIM card access) 
### Usage scenarios
* Mobile payment (credit card)
* Identification (national ID card) 
### Pass-through to websites (complexity)
* Many components may be involved:
  * website, card issuer, certificate authority, browser, secure element, helper app, …
* Difficult to debug and secure properly 

---
## 6. Computational Photography

### Goal
* Improve camera performance **beyond physical limits** 
Examples listed:
* Artificial **bokeh** effect (usually needs DSLR + large aperture)
* “Night Sight” on **Pixel 4+** (usually needs tripod + long exposure) 
### Superresolution / Superzoom (example)
* Take a burst of several images quickly (**< 1 second**)
* Merge into a final image with **2–3×** resolution/zoom of the sensor 
### Approach + challenges (as listed)
Approach:
* Use minimal shifts between images to improve details
* Example source of shifts: hand tremor measured with **IMU** (or artificial motion via **OIS**)
* Takes advantage of the **Bayer pattern** 
Challenges:
* Moving objects
* Image sensor noise
* Unpredictable motion 
### Cautionary note (slide’s point)
* “Don’t overdo it…”
* “AI” enhancement example: any blurry bright circle on black → “moon”
* Can “hallucinate” non-existent details
* Open question: how much postprocessing do we want? 

---

## Review Checklist

1. What is the Dash Button’s **setup problem**, and what are the two main solutions shown?
2. Why can Netguard do network filtering **without root** (what OS feature does it leverage)?
3. In the contact-tracing cartoon: what do phones broadcast, how long is it stored, and how do alerts happen?
4. In “Find My”: what does the AirTag broadcast, and how is location reported + decrypted?
5. Compare **HCE vs SEM**: which is less secure, and which requires extra hardware?
6. For superresolution: what’s the **core trick** and what are the **three challenges** listed?
---
## **1. The Core Problem: RSSI is not Distance**
The fundamental reason BLE contact tracing struggled is that it relies on **Received Signal Strength Indicator (RSSI)** to estimate distance. As learned in Lecture 02, signal strength is affected by absorption, reflection, and diffraction, making it a very noisy proxy for physical proximity.

---
### **2. False Positives (Warning without Infection Risk)**
**Scenario A: The "Thin Wall" Neighbor**
- **Situation:** You are sitting on your couch reading. Your neighbor, who is COVID-positive, is sitting on their couch just on the other side of the drywall separating your apartments.
- **Wireless Principle:** As discussed in **Lecture 02**, 2.4 GHz waves (BLE/WiFi) can penetrate standard building materials like drywall and wood. The signal passes through the wall effortlessly.
- **Result:** The phones detect a strong signal (high RSSI) and log a "close contact" because the signal strength suggests you are within 1-2 meters. However, the virus cannot travel through the wall. You get a red warning notification the next day for an exposure that was physically impossible.

**Scenario B: The "Traffic Light" Encounter**
- **Situation:** You are in your car at a red light with the windows rolled up. Another car pulls up right next to you (within 1.5 meters). The driver is positive.
- **Wireless Principle:** Glass allows RF signals to pass through relatively well (Lecture 02). While metal blocks signals, the windows provide a path for the BLE beacon to reach your phone.
- **Result:** The phones handshake for the duration of the red light (2-3 minutes). The app registers a high-risk contact. In reality, you are in a sealed metal-and-glass box with a separate ventilation system.
---
### **3. False Negatives (Exposure without Warning)**
**Scenario A: The "Meatbag" Absorption (Body Shielding)**
- **Situation:** You are standing in a crowded bus line, directly facing a contagious person (face-to-face, < 1m). Both of you have your phones in your _back_ pockets.
- **Wireless Principle:** Lecture 02 noted that **2.4 GHz is the resonant frequency of water** (which is why microwaves work). The human body is mostly water.
- **Result:** To reach your phone, the signal must travel through the infected person's torso and your torso. The human bodies absorb a massive amount of the signal energy. The phones perceive a very weak RSSI, interpreting it as the users being 10+ meters apart. The app filters this out as "safe distance," failing to warn you of a direct exposure.

**Scenario B: The "Metal Canyon" Reflection (Multipath)**
- **Situation:** You are in a modern train carriage or an elevator with many metal surfaces. You are standing 4 meters away from a sick person (technically "safe" by some standards, but let's say the train is poorly ventilated).
- **Wireless Principle:** Metal causes **Multipath Scattering** and **Reflection** (Lecture 02).
- **Result:** The signal bounces off the metal walls and ceiling, taking a longer path to reach your phone or interfering destructively (fading). The phone calculates the "Time of Flight" or signal strength based on this scattered path, miscalculating the distance as much further away than it is. Alternatively, destructive interference creates a "dead zone" where no packets are received at all.

---
### **4. Mitigation Strategies (Speculation)**
Based on "Alternative I/O" (Lecture 03/06) and "Wireless" (Lecture 02):
**1. Ultrasound Handshakes (Alternative I/O Channel)**
- **Concept:** Instead of relying solely on 2.4 GHz Radio, use the phone's **Speaker and Microphone**.
- **Mitigation:** The phone emits a high-frequency audio chirp (ultrasound, inaudible to humans).
- **Why it helps:** Unlike Radio waves, **sound does not travel well through glass or thick walls**. If your phone can "hear" the other phone, you occupy the same _air space_. This would eliminate the "Thin Wall" and "Traffic Light" false positives.
**2. Context Awareness via IMU (Sensors)**
- **Concept:** Use the Accelerometer and Gyroscope (Lecture 04).
- **Mitigation:** If the phone detects that it is traveling at 50 km/h (driving) or walking pace, it can adjust its sensitivity.
- **Why it helps:** If the IMU data shows zero movement for 2 hours (phone on a nightstand), the system could lower the "risk score" of fleeting signals passing by, assuming the user is stationary/indoors and protected by walls.
**3. Ultra-Wideband (UWB) (Wireless Hardware)**
- **Concept:** Newer phones have UWB chips (Lecture 02 mentions UWB/Pulse radio briefly in older contexts, but it's relevant here).
- **Mitigation:** UWB uses **Time-of-Flight (ToF)** rather than signal strength to measure distance.
- **Why it helps:** It measures exactly how long light takes to travel between devices. It is immune to the "Signal Strength" errors caused by body absorption (Scenario A False Negative), providing centimeter-level accuracy.

# Lecture 07: Introduction 
## 1. What “Interactive Surfaces & Spaces” covers
Main sections in this intro lecture:
* Definition & differentiation
* Big issues
* Research context
* Examples 
---
## 2. Definition
### Interactive Surfaces
What “surfaces” track:
* **2D position** (+ **0.5** aka “fishtank”)
* **1D rotation** 
Surfaces: **input types** (cf. **TUIO 2.0**)
* **(Multi-)Touch**: 2D positions (+ rotation, + hover)
* **Pen/stylus**: ID, 2D position, rotation, angle, pressure, hover
* **Tokens**: ID, 2D position, rotation
* **“Blobs”**: 2D position, rotation, shape 
### Interactive Spaces
What “spaces” track:
* **3D position**
* **3D rotation** 
Spaces: **input types**
* **Tracked objects**: 3D position + 3D rotation = **6D pose**
* **Tracked controllers**: 6D pose + buttons
* **Hand pose** (cf. earlier lecture): 6D pose for all joints
* **Full body pose** 

---
## 3. Differentiation questions (from the slides)
* Is a **tablet** an interactive surface? A **smartphone**?
* Is wearing an **MR headset** creating an interactive space? 

---
## 4. Big Issues
Similar to mobile devices:
* Touch-related issues
* Gestures and discoverability
Unique to ISS:
* Infrastructure requirements
* Fatigue and reachability 
---
## 5. Research Context
ISS conference series (ACM):
* More involved setup / hardware requirements
* Smaller user group than mobile devices (cf. ACM MobileHCI)
* Therefore more “research”-centric applications 
Related research areas:
* Tangible Interaction (cf. ACM TEI)
* Mixed Reality (cf. ACM VRST, IEEE VR) 

---
## 6. Examples shown
### SandScape (2002)
* Landscape simulator (with real sand/clay)
* Example application areas: hydrodynamics, weather, architecture, … 
### Reactable (2009)
* Technically a musical instrument (synthesizer)
* Interaction (mostly) through tokens/tangibles 
### Interactive ads (2017)
* Question: how to attract passersby to view a public display?
* Shows overlay of people’s silhouettes on the screen
* “Mirror” effect increases visibility 
### Virtual Valcamonica (2018)
* Visualize prehistoric rock carvings
* Multiple display + collaboration features (using shutter glasses)
* Large-scale tracking environment 
### SPLOM Wall (2020)
* SPLOM = ScatterPLOt Matrix
* Visualization of large datasets
* 4.1 m × 2.3 m wall display
* Key question: “How to reach everything?” 
### Anatomy Education (2024)
* Study of mixed reality for “embryonic anatomy education”
* “Better alone or in groups?” → requires shared space 

---
## Review Checklist
1. What’s the difference between **surfaces** and **spaces** in terms of tracked degrees of freedom?
2. List the **surface input types** (TUIO 2.0 categories) and what each provides.
3. What is a **6D pose**, and which “space” input types provide it?
4. What are the **two big-issue categories**: (a) similar to mobile, (b) unique to ISS?
5. Why is ISS research often more “research-centric” than MobileHCI (per the slides)?
6. Pick two examples and state: what system it is + what interaction or problem it highlights.

## solutions:
- **Ship Navigation: Large Interactive Surface** – Replaces the traditional chart table with a shared digital surface, allowing multiple officers to collaborate on route planning and view large-scale nautical charts simultaneously.
- **Emergency Response: Large Interactive Surface** – Provides a central "command center" wall or table where a team can gather to visualize the entire disaster area and coordinate resources on a shared map.
- **Airhockey Game: Large Interactive Surface** – Offers the necessary multi-touch capabilities and direct horizontal interaction for four players to manipulate virtual pucks simultaneously in real-time.
- **Collaborative Text Writing: Regular Laptop or Desktop Computer** – Physical keyboards are essential for efficient, precision text entry, as virtual keyboards on surfaces suffer from ergonomic issues like the "gorilla arm" effect.
- **Air Traffic Control: Mixed-Reality Space** – Allows controllers to visualize the inherently 3D data of aircraft altitudes and trajectories in a spatial environment, reducing the cognitive load of interpreting 2D radar screens.
# Lecture 08: ISS Technologies 

## 1. Overview: ISS tech stack
Two big parts:
* **Output**
  * Head-Mounted Displays (HMDs)
  * Screens & 3D glasses
  * Sound & active tangibles
* **Input**
  * Touch & tangibles
  * Depth cameras
  * 6 DoF tracking 

---
## 2. Output Technologies

### Head-Mounted Displays (HMDs)
* Used for **interactive spaces**
* (Slides point to Lecture 5 for details) 
### Screens (for interactive surfaces)
* LCD/OLED displays
* Projection screens 
### Stereoscopic screens (3D)
Core requirement:
* Need some way to show **different images** to **left vs. right eye** 
Options shown:
* **Autostereoscopic** (e.g., parallax barrier / lenticular lens)
  * Mostly **single-user**
* **Glasses-based**
  * **Shutter glasses** or **polarizing glasses**
  * Requires **special projector and/or screen** 
### Active Tangibles (tangibles as output)
* Tangible objects can also be **output devices**
* Can use **sound, light, motion, …** 
### Sound zones
* Slide raises the question: *Is this an interactive space?*
* It can be “just (steerable) sound …” 
---
## 3. Input Technologies: Touch & Tangibles
### Touch technology families
* **Resistive**
* **Capacitive**
* **Optical** 
### Resistive touch
* Cheap, low-end technology (**no multitouch**)
* Two conductive layers separated by spacers
* Can be used with **gloves, pens, …** 
### Capacitive touch
Variant 1 (common in POS terminals etc.):
* No multitouch
* Robust, simple
* Not usable with gloves 
“Projected capacitive” (two variants):
* **Mutual capacitance**: each row/column measured
* **Self capacitance**: each crossing measured individually 
### Optical touch (variants shown)
* **FTIR (Frustrated Total Internal Reflection)** (projector/camera-based)
* **Diffuse Illumination (DI)**
* **Grid-based**: IR grid + sensors on opposite sides
* **Laser rangefinder(s)**: suitable for very large screens
* **In-cell sensing**: custom LCD screen with light-sensitive pixels
  * Only one device mentioned: **Samsung SUR40**
  * Pro: can detect hands, fingers, tokens, …
  * Con: sensitive to stray light 
### Tangible technologies (optical)
* **Passive tokens**: ReacTIVision, AruCo, ByteTag, …
  * Requires a **camera-based system**
* “Inside-out” tracking with **active tangibles**
  * Needs **no camera**
  * But needs a **special surface pattern** 
### Pen / stylus input
* Most touch tech can detect pens (simulate a “fingertip”)
* Special cases:
  * **Apple Pencil / Wacom**: capacitive or wireless data channel to screen (angle, pressure, …)
  * **Anoto (discontinued) / Tiptoi**: camera in tip scans invisible pattern on paper 

---
## 4. Input Technologies: Depth Cameras
### What a depth camera provides
* Regular camera: **color** value per pixel
* Depth camera: **distance** value per pixel (often shown with a color map) 
### Geometry-based depth cameras (principle)
* Create two “views” of the scene
* Match scene points between views
* Determine angles for each scene point
* Trigonometry happens → distance 
### Geometry method 1: Stereo matching
* Two images of the scene
* Stereo matching of corresponding pixels
* Ideally only needed on horizontal scanline
* Examples listed: **Occipital Structure Sensor**, **Intel RealSense D4xx** 
### Geometry method 2.1: Speckle pattern
* Random dots pattern (random, but previously known)
* “Patches” of the pattern can be matched
* Depth resolution lower than image resolution
* Example: **Kinect v1** 
### Geometry method 2.2: Stripe pattern (Gray code)
* Alternating stripes encode a binary ID for each pixel
* Requires high frame rate or static scene (slide asks “why?”)
* Requires IR projector
* Example listed: **RealSense SR300 (~300 FPS)** 
### Time-of-Flight (ToF) depth cameras
Principle:
* Emit (infrared) flash
* Measure time until reflected light arrives
* Math happens → distance
* Example: **Kinect v2** 
Practical ToF note (from slides):
* Often measure **phase difference** (not direct time)
  * A clock signal with frequency *f* modulates:
    * IR emitter (“flash”)
    * sensitivity of light sensor
  * Result is phase difference
  * Using *c* and *f* gives distance 
### Depth–color alignment
* Many depth cameras also have a “plain” color camera
* Problem: find corresponding color for each depth pixel (or vice versa)
* Requires intrinsic + extrinsic camera parameters
  * Intrinsic: field of view, distortion, focal length, …
  * Extrinsic: translation, rotation w.r.t. origin 
### Point clouds
* Each depth pixel → 3D point (x, y, z)
* With color → (x, y, z, r, g, b) 
### Depth cameras for ISS (why useful)
* Use as a “filter”: ignore the surface itself, detect only objects
* No planar surface necessary 
---
## 5. Input Technologies: 6DoF Tracking
### Setup & hardware (as listed)
* Uses **2 or more cameras** + **asymmetric targets**
* Targets can be:
  * **Reflectors** (Vicon, ART)
  * **LEDs** (Meta, HTC)
* Note on HTC Vive:
  * Sensors on the tracker
  * Light sources in the room 
### Core idea (slides)
* Intersection of rays from ≥ 2 cameras → 3D points
* Unique point distances → target ID & orientation 
---

## Review Checklist

1. Name the **three output categories** for ISS (from the overview slide).
2. What’s the main requirement for **stereoscopic screens**, and what’s the difference between autostereoscopic vs glasses-based approaches?
3. List the **touch technology families** and one key property of each (as given on the slides).
4. What optical touch variants are listed (FTIR, DI, grid-based, laser rangefinder, in-cell sensing)?
5. What’s the difference between a regular camera and a **depth camera**?
6. Compare depth camera methods: **stereo matching**, **speckle pattern**, **stripe/Gray code**, **ToF**.
7. What do “intrinsic” vs “extrinsic” parameters refer to in depth–color alignment?
8. What does “6DoF tracking” use (cameras + targets), and what geometric idea is used to recover 3D points?


