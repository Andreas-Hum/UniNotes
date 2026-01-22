### **1. The Core Problem: RSSI is not Distance**

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