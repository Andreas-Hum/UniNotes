Based on the physics of **Frustrated Total Internal Reflection (FTIR)** covered in Lecture 07, here is the step-by-step solution to the exercise.

### **1. Calculate the Critical Angle ($\theta_c$)**

First, we determine the critical angle for the acrylic glass (PMMA) relative to the surrounding air. This is the minimum angle at which light must hit the surface to remain trapped inside the glass (Total Internal Reflection).

- Formula: The critical angle is defined by Snell's Law where the refraction angle is $90^\circ$:
    
    $$\theta_c = \arcsin\left(\frac{n_{2}}{n_{1}}\right)$$
    
    Where:
    
    - $n_{1} = 1.49$ (Refractive index of Acrylic Glass/PMMA)
        
    - $n_{2} \approx 1.00$ (Refractive index of Air)
        
- Calculation:
    
    $$\theta_c = \arcsin\left(\frac{1.00}{1.49}\right)$$
    
    $$\theta_c \approx \arcsin(0.6711)$$
    
    $$\mathbf{\theta_c \approx 42.15^\circ}$$
    

**Result:** Any light ray hitting the surface at an angle **greater than $42.15^\circ$** will be totally internally reflected and trapped in the pane.

---

### **2. Frustration Analysis for the Shoes**

For the touchscreen to detect a touch ("frustration"), the Total Internal Reflection must be broken. This allows the light to escape the glass, enter the shoe sole, scatter, and be seen by the camera below.

We analyze the interaction for both materials:

#### **Shoe A ($n = 1.3$)**

- **The Scenario:** Light attempts to pass from Glass ($n=1.49$) into Shoe A ($n=1.3$).
    
- New Critical Angle: Since $n_{shoe} < n_{glass}$, a critical angle still exists.
    
    $$\theta_{c, shoeA} = \arcsin\left(\frac{1.3}{1.49}\right) \approx \arcsin(0.8725) \approx \mathbf{60.75^\circ}$$
    
- **Conclusion:** The "frustration" (transmission of light) only occurs if the light rays hit the surface at an angle **less than $60.75^\circ$**.
    
    - If the system relies on light rays bouncing at very shallow angles (e.g., $70^\circ$ or $80^\circ$), the light will **stay trapped** in the glass (Total Internal Reflection is maintained) and the camera might not see the shoe.
        
    - It works _conditionally_, depending on the angle of the LED light.
        

#### **Shoe B ($n = 1.55$)**

- **The Scenario:** Light attempts to pass from Glass ($n=1.49$) into Shoe B ($n=1.55$).
    
- **Physics Check:** Light is traveling from a medium of _lower_ density to a medium of _higher_ density ($1.49 < 1.55$).
    
- **Conclusion:** Under these conditions, **Total Internal Reflection is impossible**. There is no critical angle. The light will _always_ refract out of the glass and into the shoe sole, regardless of the incident angle.
    
- **Result:** This guarantees "frustration" of the signal. The camera will definitely see the touch.
    

### **Final Answer**

**Shoe B is the correct answer.**

While Shoe A might work for some light rays (those between $42^\circ$ and $60^\circ$), **Shoe B** has a higher refractive index than the glass itself. This ensures that light will always escape the glass and illuminate the contact point, providing a robust signal for the FTIR system.