---
tags:
  - uni
  - mobile-systems
  - lecture-notes
  - computer-science
course: Mobile Information Systems
lecture: 01 - Big Issues
date: 2025-01-21
---

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

# Review Questions
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



---
tags: [uni, mobile-systems, lecture-notes, networks, location]
course: Mobile Information Systems
lecture: 02 - Location & Networks
date: 2025-01-21

---

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

# Review Questions
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
---
tags: [uni, mobile-systems, lecture-notes, io, ux]
course: Mobile Information Systems
lecture: 03 - I/O on Small Screens
date: 2025-01-21
---

# Lecture 03: I/O on Small Screens

## Part 1: Input (The Bottleneck)

Input is the primary bottleneck in mobile interaction. The bandwidth from User $\to$ Device is much lower than Device $\to$ User.

### 1. Keypads (Hard Keys)
Before touchscreens, physical keypads were standard.
* **12-Key Pad (ISO/IEC 9995-8):** The standard 0-9, *, # layout.
* **Text Entry Methods:**
    * **Multi-tap:** Press '2' once for 'a', twice for 'b', etc. Slow and tedious.
    * **Predictive (T9):** Press each key once. The system uses a dictionary to guess the word (disambiguation). "Good" sequences match unique words; "bad" sequences (collisions) require manual selection (e.g., "book" vs. "cool").

### 2. Touchscreens
The dominant input method today.

| Feature | Resistive (Old) | Capacitive (Modern) |
| :--- | :--- | :--- |
| **Mechanism** | Two layers pressed together (Pressure). | Measures change in capacitance (Conductivity). |
| **Input Tool** | Finger, Stylus, Fingernail (Anything). | Finger, Special Stylus (Conductive objects only). |
| **Clarity** | Lower (extra plastic layers). | Higher (glass). |
| **Multi-touch** | Generally No. | Yes. |
| **Cost** | Cheap. | More Expensive. |

### 3. Soft Keyboards
Virtual keyboards on touchscreens introduce specific challenges:
* **Lack of Haptics:** No physical "click" confirmation.
* **Occlusion:** Your hand covers the keys (and the content).
* **Fat Finger Problem:** Touch area is larger than the target.

> [!TIP] Improvements
> * **Landscape Mode:** Larger keys, but covers the whole screen.
> * **Continuous Swipe (ShapeWriter/Swype):** Draw a line through letters. Uses geometric pattern matching + dictionary. Very fast.
> * **Personalization:** Keyboards learn your slang and hit-zones over time.

### 4. Gestures
* **Bezel Swipe:** Starting a swipe from outside the screen (e.g., on the black frame) is distinct from an on-screen swipe. Used for system menus (iOS Control Center, Android Back).
* **Palm Rejection:** Software must ignore accidental touches from the palm while holding the device.

---

## Part 2: Visual Output (Displays)

Small screens mean low information density.

### The Visual Angle
To determine if a screen is "good enough" (Retina quality), we look at the **Visual Angle** ($\theta$), not just resolution. It depends on size ($S$) and distance ($D$).

$$\theta = 2 \cdot \arctan \left( \frac{S}{2D} \right)$$

* *Implication:* A phone held close needs higher PPI (Pixels Per Inch) than a TV viewed from across the room to appear equally "sharp."

### Display Technologies

#### 1. LCD (Liquid Crystal Display)
* **Mechanism:** Backlight shines through liquid crystals which rotate to block/pass light.
* **TN (Twisted Nematic):** Cheap, fast, but bad viewing angles and color.
* **IPS (In-Plane Switching):** Good colors, great viewing angles, standard for modern phones.
* **Pros/Cons:** Mature tech, but backlight is always on (no true black), consumes power even for black pixels.

#### 2. OLED (Organic Light Emitting Diode)
* **Mechanism:** Each pixel produces its own light.
* **AMOLED:** Active Matrix OLED (used in phones).
* **Pros:** Perfect blacks (pixels turn off), thinner, flexible (foldable phones!), lower power for dark content.
* **Cons:** **Burn-in** (static images leave ghosts), degrades over time (blue subpixels die fastest).
* **PenTile Matrix:** A subpixel layout (RG-BG) that shares subpixels.
    * *Result:* Lower effective resolution than claimed. Text can look "fuzzy" or have color fringes.



#### 3. E-Ink (Electrophoretic)
* **Mechanism:** Tiny capsules with black and white pigments moved by electric charge.
* **Pros:** **Bistable** (consumes power *only* when changing the image), readable in direct sunlight (reflective).
* **Cons:** Very slow refresh rate (ghosting), monochrome (usually). Best for e-readers.

---

## Part 3: Non-Visual Output

When the visual channel is overloaded (or the screen is in a pocket), we use other channels.

### 1. Audio
* **Speech:** Text-to-Speech (TTS). Good for navigation, but slow and linear.
* **Non-Speech Audio:**
    * **Earcons:** *Abstract*, musical patterns. Arbitrary mapping (must be learned).
        * *Example:* "Ding-Dong" = Doorbell. Nokia SMS tone = Morse code for "SMS".
    * **Auditory Icons:** *Metaphorical*, natural sounds. Intuitive mapping.
        * *Example:* Crumpling paper sound = Deleting a file. Typewriter sound = Typing.

### 2. Tactile (Haptics)
* **Vibration:** Binary (on/off) or patterned. Used for notifications.
* **Haptics:** Simulating texture or friction (e.g., Apple Taptic Engine).
* **Microfluidics (Tactus):** Experimental tech where physical buttons "swell" out of a flat screen, then disappear.

> [!SUMMARY] Output Comparison
> * **Visual:** High bandwidth, requires attention.
> * **Audio:** Omnidirectional (don't need to look), but intrusive and transient.
> * **Tactile:** Private, low bandwidth, good for confirmation.

---

# Review Questions
1. Compare **Earcons** vs. **Auditory Icons**. Give an example of each.
2. Why does an **OLED** screen potentially save battery compared to **LCD**, and when would it not?
3. What is the **PenTile** matrix and how does it affect the perceived quality of a display?
4. Explain the difference between **Resistive** and **Capacitive** touchscreens regarding input tools.
5. Why is **E-Ink** considered "Bistable" and what is the benefit?


---
tags: [uni, mobile-systems, lecture-notes, ubicomp, iot]
course: Mobile Information Systems
lecture: 04 - Ubiquitous Computing & IoT
date: 2025-01-21
---

# Lecture 04: Ubiquitous Computing & IoT

## 1. The Vision of Ubiquitous Computing (UbiComp)

**Mark Weiser** (Xerox PARC, 1991) is the father of UbiComp. His seminal paper "The Computer for the 21st Century" laid the groundwork.

> [!QUOTE] The Core Philosophy
> "The most profound technologies are those that **disappear**. They weave themselves into the fabric of everyday life until they are indistinguishable from it."

### The Three Waves of Computing
Weiser described computing evolution in three distinct eras:

1.  **Mainframe Era:** Many people share **one** computer. (1960s-70s)
2.  **PC Era:** **One** person has **one** computer. (1980s-2000s)
3.  **UbiComp Era:** **One** person interacts with **many** computers. (2000s-Present)



### Core Concepts
* **Disappearing Computer:** The technology fades into the background. You focus on the task, not the tool.
* **Calm Computing:** Technology that informs but doesn't demand focus. It moves easily between the periphery and the center of attention.
* **Context Awareness:** Devices understand the user's situation (location, activity, environment) and adapt accordingly.

---

## 2. The Internet of Things (IoT)

IoT is the technical realization of the UbiComp vision. It refers to networking physical objects ("things") enabling them to collect and exchange data.

* **Definition:** A global infrastructure for the information society, enabling advanced services by interconnecting (physical and virtual) things based on existing and evolving interoperable information and communication technologies.

### Enabling Technologies (The Laws)
The explosion of IoT is driven by hardware trends:
* **Moore's Law:** Processing power doubles every ~18 months (Cheaper, smaller CPUs).
* **Kryder's Law:** Storage density increases (Smaller, massive storage).
* **Gilder's Law:** Bandwidth grows 3x faster than computing power.

---

## 3. Smart Dust & WSNs

**Smart Dust:** Concept of tiny, wireless sensors (size of a grain of sand) that can detect light, temperature, vibration, etc.
* **MEMS (Micro-Electro-Mechanical Systems):** The technology that makes tiny mechanical parts (gears, mirrors, sensors) on silicon chips possible.
* **WSN (Wireless Sensor Networks):** Thousands of these "motes" communicating to form a network.

### The "Mote" Architecture
A single sensor node (mote) consists of:
1.  **Sensors:** (Temp, light, etc.)
2.  **Microcontroller:** (The brain, very low power)
3.  **Transceiver:** (Radio for communication)
4.  **Power Source:** (Battery or Energy Harvesting)

> [!WARNING] The Power Bottleneck
> Computing and sensing are cheap energy-wise. **Communication** (sending radio signals) is the most expensive operation.
> *Strategy:* Process data locally (Edge Computing) and send only the result, rather than sending raw data.

---

## 4. Identification: RFID

**Radio Frequency Identification (RFID)** is a key enabler for tracking "dumb" objects.

### Components
1.  **Tag (Transponder):** Attached to the object. Contains a chip + antenna.
2.  **Reader (Interrogator):** Sends signal to the tag and reads the response.
3.  **Backend:** Database mapping IDs to object info.



### Tag Types
| Type | Power Source | Range | Cost |
| :--- | :--- | :--- | :--- |
| **Passive** | None. Harvests energy from the Reader's signal. | Short (cm to m) | Very Cheap (~cents) |
| **Active** | On-board Battery. | Long (100m+) | Expensive (~$20+) |
| **Semi-Passive** | Battery for chip, but uses Reader energy to talk. | Medium | Medium |

### Coupling Methods (How they talk)
1.  **Inductive Coupling (Near Field):**
    * Used in Low Frequency (LF) and High Frequency (HF).
    * Works like a transformer (magnetic field).
    * Range: Very short (touch to ~1m).
2.  **Electromagnetic Backscatter (Far Field):**
    * Used in Ultra High Frequency (UHF) and Microwave.
    * Tag reflects the reader's radar signal (like a mirror).
    * Range: Longer (up to ~10m for passive).

### Frequencies
* **LF (125-134 kHz):** Animal tracking, key fobs. Slow, penetrates water/tissue well.
* **HF (13.56 MHz):** Smart cards, library books. Basis for **NFC**.
* **UHF (860-960 MHz):** Supply chain, pallet tracking. Fast, but blocked by water/metal.

---

## 5. Privacy & Security Issues

UbiComp creates a "Panopticon" (surveillance state).

* **Invisibility:** You don't know when you are being watched (sensors are hidden).
* **Comprehensive:** Tracks location, health, social interactions, purchases.
* **Langheinrich’s Principles:** Proposed guidelines for privacy in UbiComp:
    1.  **Notice:** Tell the user they are being tracked.
    2.  **Choice:** Allow opting out.
    3.  **Proximity:** Data should be local (don't send everything to the cloud).
    4.  **Anonymity:** Use pseudonyms.

---

# Review Questions
1. What is the fundamental difference between the **PC Era** and the **UbiComp Era** regarding the user-to-computer ratio?
2. Explain the difference between **Inductive Coupling** and **Backscatter** in RFID. Which one enables longer range?
3. Why is **Energy Harvesting** critical for Smart Dust?
4. How does **Mark Weiser** define a "profound technology"?
5. In a Wireless Sensor Network, why is it better to process data on the mote rather than sending raw data to the base station?

---
tags: [uni, mobile-systems, lecture-notes, hci, case-studies]
course: Mobile Information Systems
lecture: 06 - Case Studies
date: 2025-01-22
---

# Lecture 06: HCI Case Studies

This lecture explores unconventional interaction methods beyond the standard touchscreen, focusing on hands-free, socially acceptable, or invisible interfaces.

## 1. The "Itchy Nose" (Nose-Based Interaction)

**Problem:** How to interact with a wearable device (like Google Glass) without raising your hands or speaking aloud (socially awkward)?
**Solution:** Use the nose as an input device.

### Technology: Electrooculography (EOG)
* **Principle:** The eye acts as a dipole (positive cornea, negative retina). Moving the eye creates a measurable potential field on the skin.
* **Setup:** Electrodes placed on the nose pads of smart glasses.
* **Mechanism:** When you rub your nose, you slightly wiggle your glasses. This movement relative to the skin is detected by the EOG electrodes.

### Interaction
* **Gestures:** Flicking the nose (left/right) or Pushing the nose.
* **Social Acceptability:** Touching your face/scratching your nose is a common, natural human behavior. It is "invisible" interaction because observers just think you have an itch.
* **Performance:** Recognition accuracy of ~80-90%.

---

## 2. Muscle-Based Interaction (EMG)

**Problem:** How to control devices without holding anything, using the body's own capabilities.
**Solution:** Electromyography (EMG) - sensing muscle activation.

### Technology: EMG Armbands
* **Device:** e.g., The Thalmic Myo (now discontinued).
* **Mechanism:** Sensors on the forearm detect the electrical signals generated when finger/wrist muscles contract.
* **Fusion:** Often combined with an IMU (Inertial Measurement Unit) to detect arm motion (swinging) vs. muscle state (clenching).

### Applications
* **Air Guitar:** Playing invisible instruments.
* **Prosthetics:** Controlling robotic hands.
* **Discrete Input:** Clenching a fist in a pocket to silence a phone.

> [!WARNING] Challenges
> * **Fatigue:** Holding a gesture (e.g., "Fist") is tiring ("Gorilla Arm" effect).
> * **Calibration:** Signals vary wildly between users and even sweat levels.
> * **Crosstalk:** Hard to distinguish specific fingers (e.g., Ring vs. Middle finger) from the forearm surface.

---

## 3. Mobile Eye Tracking

**Problem:** Using eyes for input is fast, but eyes are primarily for *perception*, not *control*.
**The Midas Touch Problem:** If you look at something, do you want to select it? Or just look at it?

### Interaction Techniques
1.  **Dwell Time:** Stare at a button for X seconds. (Slow, tiring).
2.  **Blinking:** Blink to click. (Unnatural, breaks visual contact).
3.  **Smooth Pursuit:** The modern solution for public displays.

### Smooth Pursuit
* **Concept:** The human eye cannot move smoothly across a static background unless it is following a moving object.
* **Mechanism:**
    1.  The interface shows moving icons (e.g., floating bubbles).
    2.  The user follows the one they want with their eyes.
    3.  The system calculates the **correlation** between the eye's path and the object's path.
* **Advantages:**
    * **Calibration-Free:** Works instantly for anyone walking by.
    * **Robust:** Hard to trigger accidentally.
    * **Secure:** Can be used for PIN entry (nobody can see which moving number you are following).

---

## 4. Floor-Based Interaction (Multitoe)

**Problem:** High-resolution floor displays exist (GravitySpace), but how do we identify *who* is standing where?
**Solution:** Identify users by their shoe soles.

### Technology: FTIR (Frustrated Total Internal Reflection)
* **Setup:** A glass floor with LEDs shining into the edge.
* **Principle:** Light is trapped inside the glass. When an object (shoe) touches the surface, it "frustrates" the reflection, and light scatters downwards to a camera.
* **Result:** A high-resolution "heatmap" of pressure points on the floor.

### Interaction
* **Identification:** The texture/pattern of the shoe sole acts as a unique fingerprint.
* **User Model:** The system tracks the "sole print" to keep user identity persistent as they walk.
* **Back-of-Device Metaphor:** Imagine the floor is the *back* of a tablet. You look down at the floor, but interact as if manipulating a mobile interface.
* **Precision:** Feet are clumsy. Interaction must be low-precision (large targets).

---

# Review Questions

1.  Why is **Smooth Pursuit** superior to **Dwell Time** for public display interaction?
2.  Explain the **social acceptability** advantage of the "Itchy Nose" interface.
3.  What physical phenomenon does **FTIR** rely on for floor sensing?
4.  Why is **EMG** difficult to use for precise typing (individual finger control)?
5.  What is the **Midas Touch** problem in the context of Eye Tracking?

---
tags: [uni, mobile-systems, lecture-notes, iss, interactive-surfaces]
course: Mobile Information Systems
lecture: 07 - Interactive Surfaces & Spaces (Intro)
date: 2025-01-22
---

# Lecture 07: Interactive Surfaces & Spaces (Introduction)

This lecture shifts focus from mobile devices to **Interactive Surfaces and Spaces (ISS)**. The core idea is "The Computer in the Room" vs. "The Computer in the Pocket."

## 1. What are Interactive Surfaces?
Interactive surfaces blend the physical and digital worlds. They move beyond the "Mouse & Keyboard" paradigm (WIMP - Windows, Icons, Menus, Pointer) to **Natural User Interfaces (NUI)**.

### Characteristics of ISS
1.  **Direct Interaction:** Touching the data directly (fingers, pens, objects) rather than using a proxy device like a mouse.
2.  **Multi-touch / Multi-user:** Supporting collaboration. Multiple people interacting simultaneously on the same hardware.
3.  **Large Scale:** Often table-sized or wall-sized displays.

### The Evolution of Interaction
* **CLI (Command Line Interface):** Text-based, expert use.
* **GUI (Graphical User Interface):** WIMP, Desktop metaphor.
* **NUI (Natural User Interface):** Touch, gesture, speech. "Reality-based interaction".

> [!NOTE] Weiser's Vision Revisited
> ISS aligns with Mark Weiser's UbiComp vision: technology that weaves itself into everyday life. It transforms furniture (tables, walls) into computational devices.

---

## 2. Hardware: How do we build them?

Building a large interactive surface is different from a smartphone screen. We often use **Projectors** and **Cameras** instead of capacitive layers.

### Optical Sensing (The Dominant Method)
Most large tables use **Infrared (IR) Light** to detect touches. This avoids visual distraction because IR is invisible to the human eye but visible to cameras.

#### Core Components
1.  **Projector:** Displays the image (Visual spectrum).
2.  **Camera:** Sees the touches (IR spectrum, requires an IR-pass filter).
3.  **Illumination:** IR LEDs to light up the surface.

### Sensing Techniques (The "Big Four")

#### 1. FTIR (Frustrated Total Internal Reflection)
* **Setup:** IR LEDs shine *into the edge* of an acrylic (glass) pane.
* **Principle:** Light is trapped inside the glass by total internal reflection. When a finger touches the surface, it "frustrates" the reflection, causing light to scatter down to the camera.
* **Pros:** Very high contrast, good for "blobs" (fingers).
* **Cons:** Cannot see "hover" or objects (only things that physically touch and are somewhat oily/wet like skin).



#### 2. DI (Diffuse Illumination)
* **Setup:** IR LEDs shine *from behind* the screen (near the projector).
* **Principle:** The camera sees the shadow or reflection of objects in front of the screen.
* **Pros:** Can see objects (markers, fiducials) and hovering hands.
* **Cons:** Lower contrast, sensitive to ambient light.

#### 3. DSI (Diffused Surface Illumination)
* **Setup:** A special acrylic sheet with tiny particles inside that scatter light.
* **Principle:** Similar to FTIR, but the whole surface glows evenly. Touching it makes the finger brighter.
* **Pros:** Uniform sensing.

#### 4. LLP (Laser Light Plane)
* **Setup:** Lasers create a "sheet" of light just above the surface.
* **Principle:** Anything breaking the light sheet reflects the laser to the camera.
* **Pros:** Extremely precise, works on any flat surface (even a normal wall).

---

## 3. Software: TUIO Protocol
How does the hardware talk to the application?
* **Problem:** Standard OS events (MouseClick) don't handle 10 fingers + 3 physical objects.
* **Solution:** **TUIO (Tangible User Interface Object)** protocol.
* **Mechanism:** Sends UDP packets containing:
    * **2D Cursors:** Fingers (blobs).
    * **2D Objects:** Tagged physical items (fiducials).

---

## 4. Tangible User Interfaces (TUI)
ISS isn't just about touch; it's about **Tangibles**.
* **Definition:** "Graspable User Interfaces." Using physical objects to manipulate digital data.
* **Example:** Placing a physical knob on a screen to turn a digital volume dial.
* **Bridge:** TUIs bridge the gap between the bits (digital) and atoms (physical).

### Benefits of TUIs
1.  **Haptic Feedback:** You can feel the object.
2.  **Persistence:** The object stays there even if power goes out (unlike a digital window).
3.  **Space Multiplexing:** Different tools for different functions (vs. Time Multiplexing: one mouse for everything).

---

# Review Questions
1.  Why is **FTIR** unable to detect a hovering hand, while **DI** can?
2.  What is the **TUIO** protocol and why is it preferred over standard mouse events for ISS?
3.  Explain the concept of **"Frustrated Total Internal Reflection"**.
4.  What are the three core benefits of a **Tangible User Interface (TUI)**?
5.  Why do optical ISS systems typically use **Infrared Light** instead of visible light for sensing?


---
tags: [uni, mobile-systems, lecture-notes, iss, touch-technology]
course: Mobile Information Systems
lecture: 08 - ISS Technologies
date: 2025-01-22
---

# Lecture 08: ISS Technologies

This lecture dives deeper into the specific hardware and software technologies used to build Interactive Surfaces, covering sensing methods, object tracking, and output displays.

## 1. Touch Sensing Technologies
Before optical systems took over large screens, several electrical methods were standard.

### Resistive
* **Mechanism:** Two conductive layers separated by spacer dots. Pressure connects the layers, creating a voltage divider.
* **Types:**
    * *4-Wire:* Cheap, but one axis usually breaks first.
    * *5-Wire:* More robust, bottom layer handles both X/Y axes.
* **Pros:** Very cheap, works with *any* stylus (pressure-based).
* **Cons:** Low clarity (layers reduce light), single touch only, prone to damage.

### Surface Acoustic Wave (SAW)
* **Mechanism:** Transducers send ultrasonic waves across the glass surface. A soft finger absorbs some energy, reducing the wave amplitude at the receiver.
* **Pros:** 100% clarity (pure glass), robust.
* **Cons:** Requires "soft" input (finger) to absorb waves; hard plastic styluses won't work.

### Capacitive
* **Surface Capacitive:** Sensors at corners create a uniform field. A finger draws current, detectable at corners. Robust but limited resolution.
* **Projected Capacitive (PCT):** The modern standard (Smartphones/Tablets).
    * **Grid:** An X/Y grid of wires (often Indium Tin Oxide - ITO).
    * **Interpolation:** Can detect touches *between* wires, offering very high resolution.
    * **Multi-touch:** Natively supported.

---

## 2. Optical Sensing (Camera-Based)
For large tables/walls, we use cameras and Infrared (IR) light. This allows for massive scale and object tracking.

### The "Big Four" Techniques

#### 1. FTIR (Frustrated Total Internal Reflection)
* **Setup:** IR LEDs shine into the *edge* of the glass.
* **Action:** Light is trapped inside. A finger "frustrates" the reflection, scattering light down to the camera.
* **Result:** High contrast "blobs" against a black background. Can detect pressure (blob size increases).
* **Limitation:** Cannot see hovering objects or markers.



#### 2. DI (Diffuse Illumination)
* **Setup:** IR light shines from *behind* the screen (or reflected off the ceiling).
* **Action:** Objects cast shadows or reflect light back to the camera.
* **Result:** Can see "hovering" hands and **Fiducial Markers**.
* **Limitation:** Lower contrast, lighting must be even.

#### 3. DSI (Diffused Surface Illumination)
* **Setup:** Uses a special acrylic with tiny scattering particles inside.
* **Action:** Light entering the edge is scattered evenly across the surface. Touching it couples the light out.
* **Result:** Similar to FTIR but with more uniform response.

#### 4. LLP (Laser Light Plane)
* **Setup:** Lasers create a thin "sheet" of light ~1mm above the surface.
* **Action:** Fingers break the sheet and light up.
* **Result:** Works on *any* flat surface (even a normal wall or floor).

---

## 3. Object Tracking (Fiducials)
Cameras allow us to track physical objects tagged with markers called **Fiducials**.

### Topological Markers
* **Type:** 2D Barcodes, QR Codes.
* **Pros:** Huge number of unique IDs.
* **Cons:** Computationally expensive to decode; usually rectangular.

### Geometrical Markers (e.g., Reactivision)
* **Type:** "Amoeba" markers. A central graph of dots.
* **Mechanism:** The system identifies the ID based on the distances and angles between the center dot and leaf dots.
* **Pros:** Very fast processing, rotation invariant, "organic" shapes.



---

## 4. Software Frameworks

### TUIO Protocol
* **Standard:** A unified protocol for tables to talk to apps.
* **Transport:** Uses UDP/OSC (Open Sound Control).
* **Messages:**
    * `2Dcur`: Cursors (fingers).
    * `2Dobj`: Objects (fiducials) with ID, position, and rotation angle.

### Application Layers
* **libTISCH:** Old C++ framework, now mostly deprecated.
* **Kivy:** Modern Python framework.
    * Cross-platform (Windows, Linux, OS X, Android).
    * Native multi-touch support via TUIO or OS events.
    * GPU accelerated (OpenGL ES 2).

---

## 5. Output Technologies

### Projectors
* **Front Projection:** Easy setup, but users cast shadows on the data.
* **Rear Projection:** No shadows, but requires huge space behind the screen.
* **Correction:**
    * **Keystone (Digital):** Warps the image to fit. Losses resolution.
    * **Lens Shift (Optical):** Moves the lens. Maintains full resolution (Preferred).

### LCD Panels
* **Challenge:** You can't put a camera *behind* a standard LCD (backlight blocks it).
* **Solutions:**
    * **Edge-lit LCDs:** Allow some transparency.
    * **Switchable Glass:** Toggles between transparent (camera sees) and opaque (projector shows) at 60Hz.
    * **Wedge Optics:** Microsoft PixelSense (formerly Surface 2.0) used wedge optics to put sensors inside the LCD pixels.

---

# Review Questions
1.  Why is **Projected Capacitive (PCT)** preferred over **Resistive** screens for smartphones?
2.  Explain the difference between **Keystone Correction** and **Lens Shift**. Which preserves image quality?
3.  Why can **Diffuse Illumination (DI)** detect fiducial markers while **FTIR** cannot?
4.  What is the advantage of **Geometrical Markers (Reactivision)** over **QR codes** for interactive tables?
5.  What mechanism does **Surface Acoustic Wave (SAW)** use to detect a touch, and why doesn't it work with a hard plastic stylus?