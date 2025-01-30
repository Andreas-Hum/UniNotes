![[Pasted image 20250122074526.png]]
## **Lecture 1: Fundamentals of Software Engineering**

### **1. Core Concepts**

#### **What is Software?**
- **Definition**: Computer programs and associated documentation.
- **Types**: Developed for specific customers or for general markets.

#### **Attributes of Good Software**
- **Functionality**: Delivers required performance and functionality.
- **Maintainability**: Can evolve to meet changing needs.
- **Dependability**: Reliable, secure, and safe.
- **Usability**: Understandable and user-friendly.

#### **What is Software Engineering?**
- **Definition**: An engineering discipline focusing on all aspects of software production, from conception to maintenance.

#### **Fundamental Activities in Software Engineering**
1. **Specification**: Defining what the software should do.
2. **Development**: Designing and programming the software.
3. **Validation**: Ensuring the software meets requirements.
4. **Evolution**: Adapting software to meet changing needs.

---

### **2. Software Process Models**

#### **Waterfall Model**

- **Characteristics**:
    - Sequential process phases: Specification, Development, Validation, and Evolution.
    - Works well with stable requirements.
- **Advantages**:
    - Clear stages and deliverables.
    - Suitable for projects with stable requirements.
- **Drawbacks**:
    1. **Rigidity**: Assumes fixed requirements.
    2. **Delayed Feedback**: Customer sees results only at the end.
    3. **Risky Deployment**: "Big-bang" production rollout.

![[waterfall.png]]
#### **Incremental Development**

- **Characteristics**:
    - Develops the system in increments, adding functionality iteratively.
- **Advantages**:
    - Early delivery of parts of the system.
    - Better adaptation to changing requirements.
- **Drawbacks**:
    1. **Design Challenges**: Incremental changes can degrade architecture.
    2. **Scalability Issues**: Difficult to expand or modify.
    3. **Refactoring Costs**: Frequent design changes increase costs.
![[incre.png]]
#### **Integration and Configuration**
- **Characteristics**:
    - Focuses on configuring and integrating reusable components.

![[component.png]]

---


### **3. Requirements Engineering**

#### **Main Activities**

1. **Elicitation and Analysis**: Gathering and refining requirements.
2. **Specification**: Documenting requirements.
    - **User Requirements**: Abstract, customer-focused.
    - **System Requirements**: Detailed, developer-focused.
3. **Validation**: Ensuring consistency, completeness, and realism.

---

### **4. Verification and Validation (VV) Testing**

#### **Types of Testing**
1. **Component Testing**: Testing individual software units independently.
    - Tools like JUnit automate testing.
2. **System Testing**: Verifying interactions between components and ensuring system functionality.
3. **Customer Testing**: Testing by the end-user to uncover errors or gaps in requirements.

---

### **5. Ethical Responsibilities in Software Engineering**

#### **Professional Obligations**

1. **Confidentiality**: Respect employer and client confidentiality.
2. **Competence**: Work within your skillset.
3. **Intellectual Property**: Protect client and employer IP.
4. **Computer Misuse**: Avoid misusing technical skills for malicious purposes.

---

### **6. Challenges in Software Engineering**

#### **Key Issues**

1. **Heterogeneity**: Developing systems for diverse platforms and integrating legacy systems.
2. **Business and Social Change**: Meeting rapidly changing requirements.
3. **Security and Trust**: Ensuring dependable and secure software.
4. **Scale**: Managing projects from small embedded systems to global cloud systems.

---

### **7. Dissatisfaction with Plan-Driven Approaches**

#### **Limitations**

1. **Coping with Change**:
    
    - Difficult to adapt to evolving requirements.
    - Assumes fixed initial business needs.
2. **Adding Business Value Late**:
    
    - Value is delivered only at the end of large projects.
    - Long timelines delay benefits.
3. **Lacking Manoeuvrability**:
    
    - High overhead in planning and documentation.
    - Excessive for small or medium projects.

## **Lecture 2: Agile values, cynefin and scrum

**The Scrum Values of Courage, Focus, Commitment, Respect, and Openness**

![[Pasted image 20250119223527.png]]
### **Scrum Framework**

#### **Definition**

Scrum is a lightweight framework that helps teams and organizations generate value through adaptive solutions for complex problems.

#### **Key Principles**

1. **Adaptability**: Solutions evolve through iterations called Sprints.
2. **Collaboration**: Strong emphasis on teamwork and stakeholder involvement.
3. **Empiricism**: Decisions are based on observation, experience, and experimentation.

---

### **Scrum Roles**

#### **Scrum Team**

- **Composition**: Scrum Master, Product Owner, Developers.
    
- **Characteristics**:
    
    - Self-managing and cross-functional.
    - No hierarchies or sub-teams.
    - Typically consists of 10 or fewer members.
- **Key Attributes**:
    
    - Focused on a single **Product Goal**.
    - Decides internally on tasks and approaches.
    - Scales by splitting into multiple cohesive teams when necessary.

---

#### **Developers**

- **Role**: Responsible for creating usable increments of the product during each Sprint.
- **Accountabilities**:
    1. Planning the Sprint Backlog.
    2. Ensuring quality by adhering to the **Definition of Done**.
    3. Adapting daily towards the Sprint Goal.
    4. Holding one another accountable.

---

#### **Product Owner**

- **Role**: Maximizes product value by managing the **Product Backlog**.
- **Accountabilities**:
    1. Developing and communicating the **Product Goal**.
    2. Ordering and refining backlog items.
    3. Ensuring backlog transparency and visibility.
- **Note**: The Product Owner is the single decision-maker for the backlog and must represent stakeholders effectively.

---

#### **Scrum Master**

- **Role**: Facilitates Scrum adoption and ensures the team follows Scrum principles.
- **Responsibilities**:
    - **For the Scrum Team**:
        1. Coaching in self-management.
        2. Removing impediments to progress.
        3. Ensuring productive Scrum events.
    - **For the Product Owner**:
        1. Supporting backlog management.
        2. Facilitating stakeholder collaboration.
    - **For the Organization**:
        1. Leading and coaching Scrum adoption.
        2. Planning Scrum implementations.

---

### **Scrum Artifacts**

#### **Product Backlog**

- **Definition**: An ordered, emergent list of work items to improve the product.
- **Key Features**:
    - Items are refined into smaller, more precise tasks.
    - Includes descriptions, order, and size estimations.

#### **Increment**

- **Definition**: A concrete stepping stone toward the Product Goal.
- **Key Characteristics**:
    - Additive to prior increments.
    - Usable and verified to meet the **Definition of Done**.
    - Can be delivered before Sprint end if needed.

---

### **The Sprint**

- **Definition**: A time-boxed iteration (one month or less) where value is delivered.
    
- **Activities within a Sprint**:
    1. Sprint Planning.
    2. Daily Scrums.
    3. Sprint Review.
    4. Sprint Retrospective.
- **Guidelines**:
    - No changes that threaten the Sprint Goal.
    - Quality standards remain constant.
    - Product Backlog is refined as needed.

---

### **Agile Values**

1. **Individuals and Interactions over Processes and Tools**
    - Encourages collaboration and empowerment of team members.
    - Focuses on team dynamics over rigid processes.
2. **Working Software over Comprehensive Documentation**
    - Prioritizes delivering value through functional software.
    - Documentation is secondary to the product itself.
3. **Customer Collaboration over Contract Negotiation**
    - Promotes active involvement of customers to refine requirements.
    - Addresses assumptions and gaps early in the process.
4. **Responding to Change over Following a Plan**
    - Adapts to evolving requirements to align with customer needs.
    - Reduces risks of delivering misaligned products.

---

### **Cynefin Framework in Scrum**

#### **Definition**

The **Cynefin Framework** is a decision-making model that helps teams navigate complexity and uncertainty. It categorizes situations into five domains:

1. **Clear**: Problems with predictable solutions.
2. **Complicated**: Problems that require expertise to solve but have predictable outcomes.
3. **Complex**: Problems with unpredictable solutions that emerge through iteration and experimentation.
4. **Chaotic**: Problems that require immediate action to establish order.
5. **Confused**: Situations where the domain is unclear.

#### **Application in Scrum**

- **Complex Domain**: Scrum is highly effective in managing complex problems where requirements are uncertain and solutions emerge through iterative cycles.
- **Empiricism**: The inspect-and-adapt nature of Scrum aligns with the iterative experimentation required for complex problems.
- **Stakeholder Collaboration**: Helps teams navigate the blurred boundaries between domains, especially in dynamic environments.

---

### **Potential Industry Challenges**

#### **Product Owner Challenges**

- Lack of representation for end-users.
- Limited expertise or availability.
- Difficulty in making key decisions on functionality and acceptance criteria.

#### **Scrum Master Challenges**

- Misinterpreted as a project manager.
- Limited knowledge of Scrum or Agile practices.
- Lack of strong relationships with Product Owners and Developers.

#### **Developer Challenges**

- Key skills (e.g., UX, architecture, testing) organized outside the Scrum Team.
- Silos preventing cross-functional collaboration.


## Lecture 3: extreme programming


![[Pasted image 20250120194000.png]]

### **Definition**

Extreme Programming (XP) is an agile software development methodology emphasizing collaboration, early and frequent software delivery, and skillful development practices. It is built on four core values:

- **Communication**: Foster effective interactions among team members.
- **Simplicity**: Focus on the simplest solution that works.
- **Feedback**: Continuous testing and customer involvement for improvement.
- **Courage**: Embrace changes and tackle challenges directly.

### **XP Philosophy**

- Encourages social change by discarding outdated habits that hinder productivity.
- Emphasizes the relationship between good workplace dynamics and technical success.

---

### **Core Principles of Extreme Programming**

XP applies the principle of taking effective practices to the extreme:

- **Code reviews**: Achieved through constant **pair programming**.
- **Testing**: Involves **test-first programming (TDD)** and **continuous integration**, including customer testing.
- **Design**: Practiced as incremental and iterative design.
- **Simplicity**: Maintain the simplest design that supports current functionality.
- **Customer involvement**: Customers collaborate on-site with the team.
- **Short iterations**: Iterations are reduced to seconds, minutes, and hours (e.g., Planning Game).

---

### **12 Core Practices in XP**

1. **Planning Game**: Collaborate to decide what will be done in the next iteration.
2. **Small, Frequent Releases**: Deliver usable software often to gather feedback.
3. **System Metaphors**: Use a simple metaphor to guide system design.
4. **Simple Design**: Keep the design as simple as possible.
5. **Testing**: Prioritize automated testing and test-first programming.
6. **Frequent Refactoring**: Continuously improve and simplify code.
7. **Pair Programming**: Developers work in pairs for better quality and knowledge sharing.
8. **Team Code Ownership**: All team members share responsibility for the codebase.
9. **Continuous Integration**: Integrate and test code several times a day.
10. **Sustainable Pace**: Avoid overworking to ensure long-term productivity.
11. **Whole Team Together**: Include all necessary roles in one team (business, developers, etc.).
12. **Coding Standards**: Adhere to agreed-upon coding practices.

---

### **Phases in XP**

|**Phase**|**Purpose**|**Activities**|
|---|---|---|
|**Exploration**|Define and estimate stories for the first release.|- Prototype development  <br>- Exploratory programming  <br>- Story card creation and estimation|
|**Planning**|Agree on release date and scope.|- Release Planning Game  <br>- Story card creation and estimation|
|**Iterations to Release**|Deliver a tested system ready for release.|- Testing and programming  <br>- Iteration Planning Game  <br>- Task creation and estimation|
|**Productionizing**|Prepare the system for operational deployment.|- Documentation  <br>- Training  <br>- Marketing  <br>- Other activities for deployment|
|**Maintenance**|Enhance and fix the system.|- Includes phases for incremental releases  <br>- Build major releases|

---

### **XP Practices in Detail**

#### **Primary Practices**

1. **Sit Together**: Encourages communication and prevents silos.
2. **Whole Team Together**: Includes all roles needed for the project, fostering collaboration and a sense of unity.
3. **Informative Workspace**: Transparent and organized workspace to ensure workflow visibility.
4. **Energized Work**: Avoid burnout by maintaining a sustainable pace.
5. **Pair Programming**: Two developers work together to stay focused and solve problems collectively.

---

#### **Cycle-Based Practices**

1. **Stories**: Plan functionality in small, visible units.
2. **Weekly Cycles**: Review progress and adjust tasks weekly.
3. **Quarterly Cycles**: Plan longer-term goals, identify bottlenecks, and make improvements.
4. **Slack**: Include low-priority tasks that can be dropped if higher-priority work needs more time.

---

#### **Test-First Programming (TDD)**

1. **Write a Failing Test**: Start with a test that fails.
2. **Run the Test**: Ensure the test fails to confirm the code has not yet been implemented.
3. **Write the Code**: Write only enough code to pass the test.
4. **Run All Tests**: Ensure all tests pass; otherwise, debug and repeat.
5. **Refactor**: Simplify and improve the code to avoid duplication.

---

### **Story-Based Planning**

1. **User Stories**: Use stories to plan and structure functionality.
2. **Effort Points**: Assign effort points to estimate the complexity of each story.
3. **Velocity**: Measure how many effort points the team completes daily to estimate the total effort for a release.


## Lecture 05 Product Management, Story Mapping and Product Roadmap 

![[Pasted image 20250120213029.png]]

![[Pasted image 20250120214134.png]]

![[Pasted image 20250120214604.png]]



![[Pasted image 20250120231210.png]]



## **Lecture 6: Risk Management**

### **Definition of Risk**

- Risk is a potential problem—it might happen or not.
- Risks involve two key characteristics:
    1. **Uncertainty**: No risk is 100% certain.
    2. **Loss**: If a risk materializes, it leads to unwanted consequences or losses.

---

### **Purpose of Risk Management**

- Helps software teams understand and manage uncertainty.
- Aims to proactively identify, assess, and mitigate potential problems before they occur.

---

### **Steps in Risk Management**

1. **Risk Identification**: Recognize what could go wrong.
2. **Risk Analysis**: Assess the probability of occurrence and potential impact.
    - Exposure is calculated as:  
        Exposure $\text{Exposure (r)} = P(r) \times L(r)$ 
        where $P(r)$ is the probability, and $L(r)$ is the potential loss.
3. **Risk Ranking**: Prioritize risks based on their probability and impact.
4. **Mitigation Planning**: Develop strategies to minimize high-priority risks.
5. **Monitoring and Management**: Continuously revisit and update the risk management plan.

---

### **Types of Risks**

1. **Project Risks**: Threaten the project plan.
    - Examples: Schedule delays, budget overruns, stakeholder conflicts.
2. **Technical Risks**: Threaten software quality and delivery.
    - Examples: Ambiguous specifications, technical obsolescence, or integration issues.
3. **Business Risks**: Threaten the viability of the software.
    - Examples:
        - Market risks: Building a product no one wants.
        - Strategic risks: Misalignment with business goals.
        - Budget risks: Loss of funding or resources.
4. **Predictable Risks**: Based on past experiences (e.g., staff turnover, poor communication).
    
5. **Unpredictable Risks**: Rare and unforeseen risks that are difficult to anticipate.
    

---

### **Risk in Scrum**
Disagreement exists about whether formal risk management is needed in Scrum since many Scrum practices inherently reduce risks:

#### **Roles and Responsibilities**
- **Product Owner (PO)**: Reduces risks by ensuring stakeholder alignment and prioritizing the Product Backlog.
- **Scrum Master (SM) and Team**: Address organizational and technical risks.

#### **Scrum Events**
1. **Sprint Planning**: Aligns the team and slices tasks to reduce scope-related risks.
2. **Daily Scrum**: Identifies impediments early, fostering conversations to mitigate risks.
3. **Sprint Review**: Reduces product risks by involving stakeholders.
4. **Sprint Retrospective**: Improves team processes, reducing operational risks.

---

### **Reactive vs. Proactive Risk Management**

1. **Reactive Strategy**
    - Addresses risks only after they occur.
    - Known as the "Indiana Jones" approach: "Don't worry, I'll think of something!"
2. **Proactive Strategy**
    - Identifies and plans for risks early in the project lifecycle.
    - Steps include:
        - Risk identification.
        - Assessment of probability and impact.
        - Ranking and mitigation planning.

---

### **Principles of Risk Management**

1. **Maintain a Global Perspective**: Consider software risks within the larger context of the system and business objectives.
2. **Take a Forward-Looking View**: Plan for future risks and establish contingencies.
3. **Encourage Open Communication**: Allow stakeholders to propose risks without judgment.
4. **Integrate Risk Management**: Embed risk considerations into every phase of the software process.
5. **Emphasize Continuous Processes**: Update risks as the project evolves and new insights are gained.
6. **Develop a Shared Vision**: Align all stakeholders to ensure cohesive risk identification and assessment.
7. **Encourage Teamwork**: Pool the skills and knowledge of all stakeholders during risk management activities.

---

### **Risk Mitigation Example: Staff Turnover**

To reduce the risk of staff turnover:

- **Before the Project**:
    - Identify causes for turnover (e.g., poor working conditions, low pay).
    - Address controllable issues.
- **During the Project**:
    - Assume turnover will occur and prepare accordingly:
        - Share information widely to ensure continuity.
        - Conduct peer reviews to keep team members informed.
        - Assign backup personnel for critical roles.
        - Standardize documentation to ease transitions.

---

### **Work Products in Risk Management**

1. **Risk Mitigation, Monitoring, and Management (RMMM) Plan**:
    - Defines strategies to address high-priority risks.
2. **Risk Information Sheets**:
    - Summarizes key risks, probabilities, impacts, and mitigation plans.

---

### **Key Takeaways**

- Risk management is essential for handling uncertainty in software projects.
- Scrum inherently addresses many risks through roles and events.
- A proactive approach to risk is more effective than reacting after problems arise.
- Continuous risk evaluation ensures risks are managed throughout the project lifecycle.

risk format given x theres a rish y which will have the consequeince z

![[Pasted image 20250121172717.png]]


## **Lecture 7: Quality Management**

### **Definition of Quality Management (QM)**

Quality management encompasses all activities and processes aimed at ensuring a high-quality product. It includes:

1. **Quality Assurance (QA)**:
    - Definition of processes and standards to achieve high-quality outcomes.
    - Introduction of quality processes during manufacturing or development.
2. **Quality Control (QC)**:
    - Application of QA processes to identify and eliminate products not meeting quality standards.

Both QA and QC are essential components of QM.

---

### **Roles and Independence in Quality Management**

- **Quality Management Team**:
    - Should operate independently from the development team to maintain objectivity.
    - Reports on software quality without being influenced by development issues.

---

### **Key Components of a Quality Management Plan** (Humphrey, 1989)

1. **Product Introduction**:
    - Description of the product, target market, and quality expectations.
2. **Product Plans**:
    - Critical release dates and responsibilities.
    - Distribution and product servicing plans.
3. **Process Descriptions**:
    - Development and service processes.
    - Standards for development and management.
4. **Quality Goals**:
    - Identification of critical quality attributes and associated plans.
5. **Risks and Risk Management**:
    - Identification of risks that might affect quality and actions to address them.

---

### **Quality Validation and Verification**

#### **Validation**
- Ensures the system is **fit for use** by meeting customer expectations and needs.
- **Question**: Are we building a system that is fit for use?

#### **Verification**
- Ensures the system meets all defined **requirements**.
- **Question**: Are we building the system correctly with all requirements implemented?

---

### **Types of Quality**

1. **Product Quality**:
    - Focuses on functionality as described by functional requirements or user stories.
2. **Process Quality**:
    - Ensures quality in the way the product is developed.
3. **Expectation Quality**:
    - Non-functional requirements or software quality attributes (e.g., efficiency, usability).

---

### **Quality in Agile Development**

In agile methods, QM shifts from being document-heavy to fostering a **quality culture** where all team members share responsibility for software quality. Key practices include:

1. **Definition of Done**:
    - Team agrees on criteria for task completion.
2. **Sprint Review**:
    - PO and stakeholders validate that the sprint delivery meets expectations.
3. **Check Before Check-In**:
    - Developers organize peer code reviews before merging changes into the build system.
4. **Never Break the Build**:
    - Code changes must not cause the system to fail.
    - Developers test their changes against the entire system before committing.
5. **Fix Problems When You See Them**:
    - Any team member can directly address issues in the code, regardless of the original author.

---

### **Evolving QM in Agile Development**

- Traditional QM relies heavily on formal documentation, testing, and validation processes.
- Agile QM focuses on lightweight processes, collaboration, and immediate feedback to ensure quality.

#### **Examples of Agile QM Practices**

1. **Check Before Check-In**:
    - Programmers arrange their own code reviews.
2. **Never Break the Build**:
    - Developers test their changes to prevent system failures.
    - Fixes for broken builds take priority.
3. **Fix Problems When You See Them**:
    - Team ownership of code encourages proactive issue resolution.

---

### **Non-Functional Requirements and Software Quality Attributes**

- Often categorized as **Software Quality Attributes** or **Software Quality Factors**.
- Examples include:
    - **Efficiency**: Ensures resource optimization.
    - **Usability**: Enhances user experience.
    - **Reliability**: Maintains system functionality under various conditions.

#### **Documentation of Requirements**
- **Functional Requirements**:
    - Documented in requirement specifications (waterfall) or user stories (agile).
- **Non-Functional Requirements**:
    - Categorized and documented separately to ensure clarity.



## **Lecture 8: Agile Testing**

### **Key Concepts in Agile Testing**

1. **Validation Testing**:
    - Ensures the system performs correctly based on its expected use.
    - Uses test cases that reflect typical usage scenarios.
2. **Defect Testing**:
    - Designed to uncover system defects.
    - Often uses obscure test cases not reflective of normal use.
![[Pasted image 20250121185436.png]]
---

### **Stages of Testing**

1. **Development Testing**:
    - Conducted during development to discover bugs and defects.
    - Includes:
        - **Unit Testing**: Testing individual program units or methods.
        - **Component Testing**: Testing interfaces and interactions within related components.
        - **System Testing**: Testing the integration and interaction of components as a whole.
2. **Release Testing**:
    - Performed by a separate team on the complete system before release.
    - Focuses on ensuring stakeholder requirements are met.
3. **User Testing**:
    - Real users test the system in their own environments.
    - Types:
        - **Alpha Testing**: Early testing with a select group of users.
        - **Beta Testing**: Broader testing by a larger user group to identify problems.
        - **Acceptance Testing**: Customers decide if the software is ready for deployment.

---

### **Types of Tests in Agile**

1. **Requirements-Based Testing**:
    - Tests the system’s ability to meet specified requirements.
2. **Scenario Testing**:
    - Simulates real-world usage scenarios to derive test cases.
3. **Performance Testing**:
    - Evaluates system performance under various conditions.

---

### **Test-Driven Development (TDD)**

TDD is an incremental approach to development, where testing and coding are interwoven.
#### **Process**:
1. Identify a small increment of functionality to implement.
2. Write a failing automated test for the functionality.
3. Run the test (it should fail initially).
4. Write the code to pass the test.
5. Refactor the code while ensuring all tests pass.
6. Repeat for the next increment.

#### **Benefits of TDD**:
1. **Code Coverage**: Every segment of code is tested.
2. **Regression Testing**: A growing test suite ensures changes don’t introduce new bugs.
3. **Simplified Debugging**: Failures indicate exactly where problems lie.
4. **System Documentation**: Tests serve as documentation of functionality.

---

### **Benefits of Agile Testing**

1. **Automation**:
    - Manual testing takes too long and is error-prone.
    - Automated tests provide rapid feedback and reduce technical debt.
2. **Collaboration**:
    - Agile emphasizes a team-wide responsibility for quality.
    - Practices like **Check Before Check-In** and **Fix Problems When You See Them** promote shared accountability.
3. **Flexibility**:
    - Testing evolves with the project, accommodating continuous integration and iterative development.

---

### **Challenges and Guidelines in Agile Testing**
1. **Error Masking in Testing**:
    - Errors during testing can hide subsequent errors.
    - Inspections (manual reviews) can help identify multiple errors without execution.
2. **Key Principles**:
    - Testing reveals the presence of errors, not their absence.
    - Automated tests should be used wherever possible.
    - Tests should aim to "break" the software to identify weaknesses.

---

### **Quality through Inspections**

Inspections offer advantages over traditional testing:
1. Identify multiple issues without the need for execution.
2. Review incomplete versions of the system without additional costs.
3. Assess broader quality attributes like maintainability, compliance, and efficiency.


![[Pasted image 20250121191842.png]]

## **Lecture 9: Dual Track Agile**

### **Definition**

Dual Track Agile is an approach to agile development where two parallel tracks—**Discovery** and **Delivery**—run simultaneously. Each track serves a distinct purpose:

- **Discovery Track**: Focuses on validating ideas, hypotheses, and customer needs through fast learning and experimentation.
- **Delivery Track**: Focuses on developing and delivering high-quality, predictable software solutions.

---

### **Key Principles of Dual Track Agile**

1. **Two Tracks, Two Mindsets**:
    - **Discovery Track**: Prioritizes fast learning, idea validation, and reducing uncertainty.
    - **Delivery Track**: Focuses on predictability, quality, and delivering finished, releasable software.
2. **Seamless Integration**:
    - Validated ideas from the Discovery Track feed into the Delivery Track as clear, actionable product backlog items.
3. **Continuous Learning**:
    - Measurement and learning continue even after a feature is shipped, ensuring ongoing validation and optimization.
4. **Collaborative Discovery**:
    - Although a product manager, designer, and senior engineer often lead discovery, the entire team should participate and stay informed about progress.
5. **Agile Principles in Discovery**:
    - Discovery is iterative, adaptive, and lean, following the same principles as agile delivery.

---

### **Objectives of Dual Track Agile**

1. **Reduce Risk**:
    - Decreases the chances of building features or products that fail to meet customer or market needs.
2. **Validate Ideas Early**:
    - The Discovery Track validates hypotheses and ideas early, preventing untested ideas from clogging up Sprints.
3. **Improve Efficiency**:
    - The Delivery Track focuses on implementing well-defined and validated product backlog items, reducing rework and slowdowns.
4. **Informed Decision-Making**:
    - Ensures that decisions are based on tested, real-world data and insights from the Discovery Track.

---

### **Key Activities in the Dual Tracks**

#### **Discovery Track**

- Activities:
    - **UX Journeys**: Explore user flows and potential pain points.
    - **Prototyping**: Create lightweight prototypes for fast feedback.
    - **Customer Interviews and Surveys**: Understand customer needs and preferences.
    - **Behavioral Analysis**: Study how customers interact with the product.
    - **Usability Testing**: Validate whether the product is user-friendly.
- Goals:
    - Validate product ideas and hypotheses.
    - Refine ideas into clear, actionable backlog items.
    - Kill or pivot ideas that fail validation.

#### **Delivery Track**

- Activities:
    - **Development**: Build the software based on validated backlog items.
    - **Testing**: Ensure quality through unit, integration, and system testing.
    - **Performance Optimization**: Focus on scalability, maintainability, and reliability.
- Goals:
    - Deliver releasable, high-quality software.
    - Ensure alignment with customer requirements.

---

### **Strengths of Dual Track Agile**

1. **Efficient Discovery**:
    - Validates ideas before they enter the Delivery Track, reducing wasted effort.
2. **Clarity in Backlogs**:
    - Refined, validated tasks in the product backlog lead to smoother Sprints.
3. **Reduced Sprint Risks**:
    - Prevents unvalidated ideas from obstructing Sprint progress.
4. **Improved Development Flow**:
    - Delivery is streamlined with well-prepared, actionable backlog items.
5. **Reality Checks for Ideas**:
    - Ensures novel ideas are tested and validated before significant investment.

---

### **Kanban in Dual Track Agile**

Kanban is often used in the Discovery Track for visualizing and managing workflow.

#### **Key Features of Kanban**:

1. **Visualize Workflow**:
    - Work items are represented on a Kanban board, showing their state and progress.
2. **Limit Work in Progress (WIP)**:
    - Restrict the number of tasks in progress to prevent bottlenecks.
3. **Measure Lead Time**:
    - Optimize processes to minimize the average time needed to complete tasks.

---

### **Examples of Dual Track Agile Process**

1. **Discovery Workflow**:
    - Discovery Backlog → Kanban (or Scrum) → Validated Ideas.
    - Discovery tasks are managed iteratively, focusing on learning and validation.
2. **Delivery Workflow**:
    - Product Backlog → Scrum Sprints (1–4 weeks) → Releasable Software.
    - Delivery builds on validated ideas to create functional, high-quality software.

---

### **Why Use Dual Track Agile?**

- Addresses the uncertainty of complex product ideas by separating **idea validation** (Discovery) from **product development** (Delivery).
- Ensures only validated, high-value ideas enter the Delivery Track.
- Aligns the product team with real customer needs and market demands.


![[Pasted image 20250121202635.png]]![[Pasted image 20250121202847.png]]


## **Lecture 10: Configuration Management and DevOps**

### **Configuration Management (CM)**

#### **Definition**

Configuration management focuses on the policies, processes, and tools required to manage changes in software systems. It is essential for ensuring consistency, tracking changes, and managing software evolution effectively.

---

### **Core Activities of Configuration Management**

1. **Change Management**
    - Tracks change requests from customers and developers.
    - Assesses costs, risks, and impacts of changes.
    - Decides when and how to implement changes.
2. **Version Management**
    - Tracks multiple versions of system components.
    - Prevents interference between changes made by different developers.
    - Tools:
        - **Centralized Systems**: Single master repository (e.g., Subversion).
        - **Distributed Systems**: Multiple repositories (e.g., Git).
3. **System Building**
    - Combines components, data, and libraries to create an executable system.
    - Frequent builds ensure bugs introduced by recent changes are caught early.
4. **Release Management**
    - Prepares software for external release.
    - Tracks released versions and maintains documentation, configuration files, and executables.

---

### **Key Concepts in Configuration Management**
- **Codeline**: Set of versions for a software component.
- **Baseline**: A collection of component versions that make up a system.
- **Mainline**: Sequence of baselines representing different system versions.

---

### **Change Request Assessment**

When deciding whether to approve a change:

1. **Consequences of Not Making the Change**:
    - If the change addresses a system failure, its priority depends on the severity of the failure.
2. **Cost and Risk**:
    - Evaluate the time, resources, and potential impacts involved in implementing the change.

---

### **Version Control Systems**

1. **Centralized Systems**
    - Single master repository for all versions.
    - Example: Subversion (SVN).
2. **Distributed Systems**
    - Multiple repositories allow developers to work independently.
    - Example: Git.

---

### **DevOps and Configuration Management**

#### **DevOps Definition**
DevOps integrates software development and IT operations, aiming to shorten development cycles, increase deployment frequency, and ensure reliable releases.

---

### **Core Phases in DevOps**

1. **Build**
    - Tools support fast workflows and automation.
    - Continuous integration (CI) merges and tests code frequently.
2. **Continuous Delivery**
    - Automates deployment pipelines.
    - Developers integrate and validate code changes daily to enable low-risk releases.
3. **Automation in Deployment**
    - Automates environment creation, configuration, and deployment using tools like:
        - **Infrastructure as Code**: Puppet, Chef, Ansible, Salt.
        - **Containers**: Docker, Kubernetes.
        - **Cloud Services**: AWS, Google Cloud, Azure.

---

### **Lean Principles in DevOps**

1. **Eliminate Waste**: Avoid activities that do not add customer value.
2. **Amplify Learning**: Encourage continuous learning and feedback.
3. **Defer Commitment**: Make decisions when facts are clear.
4. **Deliver Fast**: Accelerate delivery to gather quick feedback.
5. **Empower Teams**: Trust and motivate team members.
6. **Build Quality In**: Automate testing and standardize processes.
7. **Optimize the Whole**: Improve overall system efficiency.

---

### **Key Metrics: Lead Time and Processing Time**

1. **Lead Time**:
    - Starts when a request is made and ends when it is fulfilled.
2. **Processing Time**:
    - The active time spent working on the request, excluding wait times.

---

### **Continuous Integration and Deployment Best Practices**

- **Fast Feedback**: Ensure quick testing and validation cycles.
- **Small Code Changes**: Reduce risks by integrating smaller, incremental updates.
- **Automation**: Use automated tests and pipelines to validate code constantly.
- **Monitor Deployments**: Generate useful telemetry and feedback after deployment.

---

### **Plan-Driven vs. Agile Configuration Management**

|**Aspect**|**Plan-Driven**|**Agile**|
|---|---|---|
|**Focus**|Documents and code|Code|
|**Activities**|Change management, version control, automated build|Version control, automated build|
|**Responsibility**|CM team, CM board|Programmers|
|**Process**|Formal, managed|Informal, integrated with practice|
|**Outcome**|CM audit (documented product control)|Next release|
|**Importance**|Indispensable for medium and large projects|Indispensable for all projects|

---

### **Benefits of Effective Configuration Management in DevOps**

1. Ensures consistency across environments.
2. Reduces risks associated with frequent releases.
3. Speeds up workflows through automation.
4. Maintains a comprehensive history of changes and versions.
5. Supports collaborative work in distributed teams.


## **Lecture 11: How It All Ties Together**

### **Requirements Elicitation**

#### **Purpose**

The aim of requirements elicitation is to understand stakeholders' work, needs, and how a system can support or improve it. This involves gathering information about:

- The application domain.
- Work activities and workflows.
- Desired system features and services.
- Constraints such as hardware or regulatory requirements.

---

### **Challenges in Requirements Elicitation**

1. **Unclear Stakeholder Needs**:
    
    - Stakeholders may struggle to articulate their needs or have unrealistic expectations.
2. **Implicit Knowledge**:
    
    - Stakeholders express requirements in their domain-specific language, making it hard for engineers to interpret.
3. **Diverse and Conflicting Requirements**:
    
    - Multiple stakeholders often have conflicting needs, requiring negotiation and prioritization.
4. **Political Influence**:
    
    - Managers or other stakeholders may push for specific features for personal or organizational reasons.
5. **Dynamic Environment**:
    
    - Changes in business priorities or the involvement of new stakeholders can introduce new requirements.

---

### **Requirements Elicitation Process**

1. **Discovery and Understanding**:
    
    - Interaction with stakeholders to uncover explicit and implicit requirements.
2. **Classification and Organization**:
    
    - Group and structure requirements into cohesive clusters.
3. **Prioritization and Negotiation**:
    
    - Resolve conflicts and rank requirements by importance and feasibility.
4. **Documentation**:
    
    - Clearly record and structure requirements for validation and development.

---

### **Techniques in Requirements Elicitation**

1. **Interviews**:
    
    - **Closed Interviews**: Predefined questions for structured responses.
    - **Open Interviews**: Flexible discussions to uncover deeper insights.
2. **Observation (Ethnography)**:
    
    - Observe stakeholders in their work environment to:
        - Identify real workflows.
        - Understand cooperative and collaborative activities.
3. **Scenarios**:
    
    - Detailed narratives of system-user interactions, including:
        - Initial conditions.
        - Normal workflows.
        - Error handling.
        - System state at the end.

---

### **Agile and Plan-Driven Methods**

#### **Key Observations**

1. **No Silver Bullet**:
    
    - Neither method is universally superior; each has its strengths and weaknesses.
2. **Home Grounds**:
    
    - Agile suits dynamic, high-change environments with smaller teams.
    - Plan-driven methods are better for large-scale, stable projects needing high assurance.
3. **Future Trends**:
    
    - Hybrid approaches that combine agility and discipline are increasingly favored.

---

### **Comparison: Agile vs. Plan-Driven Methods**

|**Characteristic**|**Agile**|**Plan-Driven**|
|---|---|---|
|**Primary Goal**|Rapid value delivery; responding to change|Predictability, stability, high assurance|
|**Team Size**|Small|Large|
|**Environment**|Dynamic, high-change|Stable, low-change|
|**Requirements**|Informal, evolving|Formal, fixed|
|**Planning**|Adaptive, qualitative|Documented, quantitative|
|**Testing**|Continuous, automated|Formalized, planned|
|**Culture**|Comfort with flexibility|Comfort with order and policies|

---

### **Cockburn's Levels of Software Method Understanding**

|**Level**|**Description**|
|---|---|
|**Level 3**|**Method Innovators**: Able to break or revise existing methods to fit unprecedented situations. Innovators who can design or adapt methodologies to meet unique needs.|
|**Level 2**|**Method Tailors**: Capable of tailoring an existing method to fit new but precedented situations. These individuals can adjust methodologies without breaking their underlying rules.|
|**Level 1A**|**Discretionary Practitioners**: With experience and training, can perform complex method steps such as sizing stories, composing patterns, or managing complex integrations. This level demonstrates proficiency and a solid understanding of methodologies.|
|**Level 1B**|**Procedural Practitioners**: Able to follow well-defined, procedural steps (e.g., writing simple code, performing basic refactoring, or adhering to coding standards). With experience, they can grow into Level 1A.|
|**Level -1**|**Non-Collaborators**: Individuals with technical skills but lacking the ability or willingness to collaborate or follow shared methodologies. These individuals can hinder team performance.|

---

### **Key Concepts of the Cockburn Framework**

1. **Collaboration and Adaptability**:
    - Agile methodologies, like Scrum or XP, rely heavily on team collaboration. Teams need members who are adaptable and capable of working together to overcome challenges.
    - For example, Levels 2 and 3 are critical for agile methods, as they involve revising and tailoring processes to fit dynamic project needs.
2. **Training and Experience**:
    - Lower levels (1A, 1B) may lack the knowledge to adapt methods but can still execute defined tasks effectively.
    - With proper training and experience, individuals can progress to higher levels.
3. **Methodology Flexibility**:
    - Cockburn’s framework highlights the need for methodologies that can accommodate teams with varying skill levels. Agile projects often require a mix of Level 1A and 2 team members for success.
4. **Team Composition**:
    - Projects that require extensive innovation and problem-solving benefit from higher-level practitioners (Levels 2 and 3).
    - Plan-driven approaches can better accommodate lower-level practitioners (1B), as tasks are predefined and heavily procedural.
---

### **Five Axes to Evaluate Agile vs. Plan-Driven**

1. **Application Characteristics**:
    - Agile: Rapid development with evolving needs.
    - Plan-driven: Predictable systems requiring stability.
2. **Team Composition**:
    - Agile: Collaborative, self-organizing teams.
    - Plan-driven: Structured teams with defined roles.
3. **Customer Involvement**:
    - Agile: Frequent, close interaction with stakeholders.
    - Plan-driven: Formalized, periodic interactions.
4. **Management Style**:
    - Agile: Empowered teams, minimal managerial oversight.
    - Plan-driven: Managerial control with detailed documentation.
5. **Development Practices**:
    - Agile: Incremental, iterative development with continuous refactoring.
    - Plan-driven: Comprehensive up-front design and longer increments.

---

### **Fred Brooks’ Software Engineering Werewolf**

Fred Brooks identified four essential difficulties in software engineering:

1. **Complexity**: Software systems are inherently intricate.
2. **Conformity**: Software must integrate with non-uniform systems.
3. **Changeability**: Requirements evolve continuously.
4. **Invisibility**: Software’s intangible nature makes it difficult to visualize and communicate.

---

### **Development Models**

1. **Waterfall Model (Plan-Driven)**:
    
    - Sequential phases: Specification → Design → Implementation → Testing → Operations.
2. **Incremental Development (Agile or Plan-Driven)**:
    
    - Iterative delivery of smaller increments.
    - Agile adapts increments based on progress; plan-driven defines increments upfront.
3. **Integration and Configuration (Hybrid)**:
    
    - Systems built from reusable, configurable components.

---

### **Key Takeaways**

1. **Complementary Strengths**:
    - Agile and plan-driven methods excel in different contexts.
2. **Requirements Elicitation Challenges**:
    - Diverse stakeholders, implicit knowledge, and evolving priorities make elicitation difficult.
3. **People Matter**:
    - Success depends heavily on collaboration, adaptability, and effective communication, as highlighted by Cockburn’s levels.
4. **Hybrid Approaches**:
    - Combining agility and discipline allows teams to balance flexibility and structure, addressing both dynamic and stable environments.

![[Pasted image 20250122070453.png]]

![[Pasted image 20250122072405.png]]


![[Pasted image 20250122073116.png]]
![[Pasted image 20250122073309.png]]
![[Pasted image 20250122074407.png]]



### **1: Software Process Model – Waterfall / Incremental / Iterative**

---

#### **Example Questions**

1. **What is Software Engineering (SE) a response to?**
    - SE addresses challenges such as **complexity** in systems and the high **failure rates** in software projects.
2. **What are the SE process activities?**
    - **Specification**: Defining system functionality and constraints.
    - **Design**: Structuring the system architecture and components.
    - **Development**: Implementing the design.
    - **Validation**: Ensuring the software meets user requirements.
    - **Evolution**: Modifying the software to adapt to changing needs.
3. **What is a software process model?**
    - A software process model is a **set of related activities** that guides the development of a software product.
4. **Describe the characteristics of the Waterfall Model.**
    - Sequential stages: Each phase (e.g., requirements, design, coding, testing) must be completed before the next begins.
    - Work products are handed off between phases.
    - **Milestones** are used to monitor progress.
5. **Describe the Incremental/Iterative Model.**
    - Breaks the system into smaller **slices or increments**, which are developed and delivered iteratively.
    - Each slice represents a subset of system functionality.
6. **When should you consider using the Waterfall Model?**
    - For projects with:
        - **Embedded systems**.
        - **Life-critical systems** (e.g., medical devices).
        - Very **large systems** with well-defined requirements.
7. **How can I determine if incremental/iterative or waterfall fits me?**
    - Use Boehm’s **Home Ground Decision Tool**, which considers factors like criticality, dynamism, team size, and personnel expertise.
8. **Describe how the Incremental Model works. Can it be plan-driven or iterative?**
    - Each increment delivers a working subset of the system.
    - It can be **plan-driven** (predefined increments) or **iterative** (feedback drives future increments).
9. **What are the advantages of the Incremental/Iterative Model?**
    - **Lower cost of changes** in requirements.
    - **Faster feedback** from users.
    - Customers receive part of the product **early** and can start deriving value.
10. **What disadvantages are there?**

- Progress is often **invisible** without documentation, making it harder to justify to management.
- **Infrastructure deterioration** may occur as new increments are added.

---

### **2: Comparison of Plan-Driven and Agile**

---

#### **Example Questions**
1. **What is the difference between plan-driven and agile?**
    - **Plan-driven**: Aims to **predict** and achieve predefined outcomes.
    - **Agile**: Accepts that change is inevitable and focuses on frequent **inspection, adaptation**, and delivering value iteratively.
2. **How do Boehm and Turner define primary factors?**
    - **Application**: Agile fits small, dynamic, and turbulent environments.
    - **Management**: Agile uses on-site customers and qualitative control.
    - **Technical**: Agile relies on informal, prioritized requirements and simple design.
    - **People**: Requires **Cockburn Level 2 and 3 developers** who are collaborative and skilled.
3. **What is the meaning of the 5 axes in the Home Ground Decision Tool?**
    - **Criticality**: The degree of risk if the software fails.
    - **Personnel**: The skill and experience level of team members.
    - **Dynamism**: The frequency of changes in requirements or environment.
    - **Culture**: Team preferences for flexibility (agile) or structure (plan-driven).
    - **Size**: Smaller teams favor agile; larger teams benefit from plan-driven approaches.
4. **Why do requirements change?**
    - **Business needs** evolve.
    - **Technology advances** introduce new possibilities.
    - Teams **learn** from early development and adapt.
5. **What is continuous integration in Agile, and how does it differ from prototype development?**
    - Continuous integration involves maintaining a **shippable product** at all times, integrating small changes regularly.
    - Prototypes are often **disposable** and not intended for production.
6. **What are XP practices?**
    - **Customer on-site**: Close collaboration with stakeholders.
    - **Pair programming**: Two developers working together on the same code.
    - **Planning game**: Involves prioritizing user stories.
    - **TDD (Test-Driven Development)**: Writing tests before code.
    - **Continuous integration**: Frequent integration of changes into the codebase.
    - **Sustainable pace**: Avoiding burnout with reasonable workloads.
7. **Scrum vs. Plan-Driven Roles**:
    - Scrum: Roles like **Product Owner (PO)**, **Scrum Master (SM)**, and **Team Members**.
    - Plan-driven: Multiple specialized roles (e.g., managers, QA, business analysts).
8. **Scrum Practices**:
    - **Sprint Planning**: Define goals and tasks for the sprint.
    - **Daily Scrum**: Daily stand-up meeting for progress updates.
    - **Sprint Review**: Demonstrate the increment to stakeholders.
    - **Sprint Retrospective**: Reflect on the sprint and identify improvements.
    - **Backlog Refinement**: Continuously updating and prioritizing backlog items.
9. **Agile vs. Plan-Driven Artifacts**:
    - Agile: **Product Burndown**, **Sprint Burndown**, **Scrum Board**.
    - Plan-driven: **Project Plan**, **Gantt Chart**, **Requirements Specification**.
10. **Plan-Driven Counterparts**:
    

- **Predict what to deliver**: Predefined milestones and specifications.
- **Plan the work**: Rely on detailed schedules and work breakdown structures.
- **Work the plan**: Follow the plan meticulously to meet deliverables.
- **Knowledge sharing**: Heavy use of documentation for communication.
### **3: Key Features of Scrum**

---
#### **Example Questions**

1. **What is Scrum?**
    - Scrum is an **iterative agile method** for managing complex software development projects.
2. **Describe essential elements of Scrum.**
    - **Scrum Roles**:
        - **Product Owner (PO)**: Defines product goals, prioritizes backlog, and represents stakeholders.
        - **Scrum Master (SM)**: Facilitates the Scrum process, ensures the team adheres to Scrum principles, and removes impediments.
        - **Team**: A cross-functional, self-organizing group responsible for delivering the product increment.
    - **Scrum Practices**:
        - **Sprint Planning**: Define sprint goals and select backlog items.
        - **Daily Scrum**: A short, daily meeting to synchronize efforts and address blockers.
        - **Sprint Review**: Demonstrate the increment and gather feedback.
        - **Sprint Retrospective**: Reflect on the sprint and identify improvements.
        - **Backlog Refinement**: Ongoing activity to clarify and prioritize backlog items.
    - **Scrum Artifacts**:
        - **Product Burndown Chart**: Tracks the remaining work toward the product goal.
        - **Sprint Burndown Chart**: Tracks the team’s progress within a sprint.
        - **Scrum Board**: Visualizes tasks in progress and their status.
3. **What is the focus of Scrum in the development process?**
    
    - Scrum focuses on an **empirical process** based on the three pillars:
        - **Transparency**: Everyone has visibility into the work and progress.
        - **Inspection**: Regularly assess the progress.
        - **Adaptation**: Adjust plans based on findings.
4. **Can you mention one or more Core Values in Scrum?**
    
    - **Commitment**: Dedication to the iteration goal.
    - **Focus**: Concentrating on sprint priorities.
    - **Openness**: Transparency about work and progress.
    - **Respect**: Team members trust and value each other’s contributions.
    - **Courage**: Trusting the team and being bold enough to take responsibility.
5. **Can you mention some typical errors or mistakes in the use of Scrum?**
    
    - **Misinterpreting Scrum Master role**: Treating them as a manager instead of a facilitator.
    - **Lack of customer involvement**: Customers not participating in iterations.
    - **Scope creep**: Adding new tasks or requirements during an active sprint.
6. **Can you say something about Extreme Programming (XP) and what techniques fit Scrum?**
    
    - XP practices align with Scrum, such as:
        - **Customer on-site**: Collaboration with stakeholders.
        - **User stories**: Simplified requirements definition.
        - **Planning game**: Prioritizing features.
        - **Test-Driven Development (TDD)**: Writing tests before code.
7. **How do Boehm and Turner define the primary factors to balance plan-driven and agile?**
    
    - **Application**: Agile suits small, rapidly changing environments.
    - **Management**: Agile relies on on-site, qualitative control, and tacit knowledge.
    - **Technical**: Informal, prioritized requirements and simple design.
    - **People**: Collaborative, skilled developers (Cockburn Level 2 and 3).
8. **Why do requirements change?**
    
    - Changes occur due to evolving **business needs**, **technological advancements**, and **user feedback**.
9. **How can you manage requirements and requirements changes?**
    
    - Use a **change process**, analyze the **impact**, and update the backlog as needed.

---

### **4: Key Features of Extreme Programming (XP)**

---

#### **Example Questions**

1. **What is Extreme Programming (XP)?**
    - XP is an **agile method** that emphasizes iterative and incremental development, collaboration, early software creation, and best development practices.
2. **What values is XP based on, according to Larman?**
    - **Communication**, **Simplicity**, **Feedback**, **Courage**.
3. **How is Extreme Programming (XP) extreme?**
    - XP applies practices to the **extreme**:
        - If testing is good → test constantly (TDD).
        - If simplicity is good → always implement the simplest solution.
        - If feedback is good → gather it frequently.
4. **Name some of the key practices in XP.**
    - **Unit Testing**: Ensures each component works as intended.
    - **Pair Programming**: Two developers collaborate on the same task.
    - **Customer On-Site**: Stakeholders are directly involved.
    - **Continuous Integration**: Regularly merging code changes.
    - **Test-Driven Development (TDD)**: Write tests before implementation.
5. **What is a user story?**
    - A **brief feature request** written as a **promise for a conversation** to clarify details. Typically written on a card.
6. **What is the format of a user story?**
    - **“As a \[user\], I want \[feature\], so that \[reason\].”**
    - Includes **acceptance criteria** for validation.
7. **How does XP describe the lifecycle of a system?**
    - **Exploration**: Discovering and estimating features.
    - **Planning**: Defining release dates and goals.
    - **Iterations to First Release**: Incremental development of a tested system.
    - **Production**: Preparing for deployment.
    - **Maintenance**: Enhancing and fixing the system.
8. **What is the iteration called in XP?**
    - It is simply called an **Iteration**.
9. **What is Test-Driven Development (TDD)?**
    - A **work cycle** where you:
        - Write a failing test.
        - Implement the simplest code to pass the test.
        - Refactor the code for simplicity and maintainability.
10. **Why is Test-Driven Development (TDD) good?**
    - **Benefits of TDD**:
        - Provides a **safety net** for changes.
        - Reduces the **cost of defects**.
        - Encourages small, manageable steps.
        - Improves **code quality** (e.g., readability, maintainability).
        - Lessens fear of breaking existing functionality.

### **5: Requirements Elicitation, Refinement, and Dual Track Agile**

---

#### **Example Questions**

1. **What main requirement activities are there?**
    - **Elicitation and Analysis of Needs**: Understand what stakeholders require.
    - **Specification of Requirements**: Clearly define requirements.
    - **Validation of Requirements**: Ensure requirements are correct and feasible.
2. **What are the steps in requirements elicitation?**
    - **Discovery & Classification**: Identify stakeholders and understand their needs.
    - **Categorization**: Group requirements into meaningful clusters.
    - **Prioritization & Negotiation**: Resolve conflicts and rank requirements.
    - **Documentation**: Record requirements for future reference.
3. **Why is it difficult to elicit requirements?**
    - **Diverse Stakeholders**: Conflicting needs from multiple stakeholders.
    - **Communication Barriers**: Stakeholders and engineers may use different terminologies.
    - **Tacit Knowledge**: Unconscious actions and knowledge are hard to articulate.
    - **Language Differences**: Stakeholders and engineers "speak different languages."
4. **What techniques can be used to elicit requirements?**
    - **Interviews**: Formal (closed) or informal (open) discussions with stakeholders.
    - **Ethnography**: Observing stakeholders in their natural work environments.
    - **Prototypes**: Interactive or visual representations to gather feedback.
5. **What is a recognized way to communicate requirements?**
    - **Stories / Scenarios**: Narrative examples of system use.
6. **How are requirements documented?**
    - **Waterfall**: Approved requirements document with strict change management.
    - **Scrum**: Product vision and backlog, updated every sprint.
    - **Product Planning**: Vision, release plans, and roadmaps.
    - **XP**: User stories.
7. **How are requirements negotiated with stakeholders?**
    - **Waterfall**: Negotiated upfront during the requirements phase (finality is crucial).
    - **Scrum**: Ongoing backlog refinement; prioritize what's most important now.
    - **XP**: Customer on-site enables constant feedback.
8. **What is agile planning?**
    - Agile planning welcomes changes and works from a **prioritized product backlog**, constantly refined based on learning.
    - **Scrum**: Sprint planning.
    - **XP**: The planning game.
9. **How can we estimate work?**
    - **Experience-Based Estimation**: Techniques like planning poker.
    - **Algorithmic Estimation**: Using models for predictions.
    - **Velocity-Based Estimation**: Measured team performance in story points.

---

### **6: Risk Management**

---

#### **Example Questions**

1. **What is a risk?**
    - A **risk** is something that might happen and result in a **loss**.
2. **Provide examples of risks and their categories.**
    - **Categories**:
        - **Project Risks**: Schedule delays, key team member departure.
        - **Technical Risks**: Integration issues, technology obsolescence.
        - **Business Risks**: Market changes, loss of budget.
3. **How do you do risk analysis?**
    - **Steps**:  
        a. **Identify Risks**: List potential risks.  
        b. **Calculate Risk Exposure (RE)**:
        - Formula: $RE = Probability \times Loss$
            c. **Prioritize Risks**: Focus on high-exposure risks.  
            d. **RMMM Plan**:
        - **Mitigation Plan**: Prevent the risk from occurring.
        - **Contingency Plan**: Manage the risk if it happens.
        - **Monitoring Plan**: Track the risk's development.
4. **How is risk management part of project management?**
    
    - **Waterfall / Plan-Driven**:
        - Risks are included in project plans.
        - Plans help identify and address risks.
    - **Agile**:
        - Risks are inspected and adapted regularly.
        - **Daily Scrum**: Impediments surface risks.
        - **Sprint Review**: Addresses product risks.
        - **Sprint Retrospective**: Focuses on process risks.
5. **What is the spiral model, and how is it related to risk management?**
    - The **Spiral Model** uses prototypes to assess risks iteratively.
    - Allows teams to evaluate and mitigate risks at every stage.
6. **What are Boehm’s primary risks?**
    - **Personnel Shortcomings**: Lack of skills or availability.
    - **Unrealistic Schedule**: Overly optimistic deadlines.
    - **Wrong Functionality**: Incorrect or irrelevant features.
    - **Budget Risks**: Funding issues or cuts.
    - **Technology Risks**: Obsolete or untested technologies.

### **7: Quality Management**

---

#### **Example Questions**

1. **How can quality be defined?**
    - Quality is the correspondence between the **experience** and **expectation** of a product.
2. **How is quality assured?**
    - Quality is assured by planning **how** and **when** to conduct **verification** and **validation** activities.
3. **What is Verification and Validation (V&V)?**
    - **Verification (VER)**: Ensures the product complies with specifications.
    - **Validation (VAL)**: Ensures the product is fit for use.
4. **What techniques do we typically use for verification and validation?**
    - **Verification**: Testing (e.g., unit tests).
    - **Validation**: Review or evaluation (e.g., usability tests).
5. **What are inspections and tests good for?**
    - **Inspections**:
        - Simplify debugging by identifying issues early.
        - Enhance code coverage.
        - Provide documentation.
    - **Tests**:
        - Ensure code reliability.
        - Enable regression testing.
6. **Why can’t we have all quality attributes?**
    - Trade-offs are necessary (e.g., **reusability** vs. **efficiency**).
7. **What is the V-model?**
    - The V-model shows relationships between testing at different levels and primary activities driving the tests:  
        a. Acceptance Testing.  
        b. System Testing.  
        c. System Integration Testing.  
        d. Sub-System Integration Testing.  
        e. Unit Testing.
8. **What should be considered when writing unit tests?**
    - Show the component works.
    - Reveal defects.
    - Cover possible inputs and outputs (partition test data).
9. **What agile practices support V&V?**
    - **Definition of Done**.
    - **Sprint Review**.
    - **Check before check-in**.
    - **Never break the build**.
    - **Fix problems when you see them**.
    - **XP Practices**: Customer on-site, Pair programming.
10. **How does Pair Programming help ensure quality?**
    

- Ongoing **peer-review** improves code quality continuously.

---

### **8: Testing**

---

#### **Example Questions**

1. **What is testing?**
    - A set of practices that supports **Verification and Validation (V&V)**.
2. **What is the purpose of testing?**
    - Ensure the program functions as intended.
    - Discover bugs before deployment.
3. **What is an example of a test supporting verification and validation?**
    - **Verification**: Unit test, component test.
    - **Validation**: Prototype test, user acceptance test.
4. **What is peer review?**
    - Evaluation of work by peers with similar competencies, typically focusing on documents or static code analysis.
5. **What is the difference between review and test?**
    - **Review**: Static; no interaction between identified errors.
    - **Test**: Dynamic; errors can lead to side-effects masking other bugs.
6. **When is either review or test good?**
    - **Review**: Best for documents, designs, and plans.
    - **Test**: Best for dynamic functionality of programs.
7. **What is the test focus of a unit test, integration test, and acceptance test?**
    - **Unit Test**: Verify valid and invalid inputs.
    - **Integration Test**: Ensure interface compatibility.
    - **Acceptance Test**: Validation through exploratory testing.
8. **When is testing done?**
    - **Plan-driven**: At the end (dedicated test team as part of QA).
    - **Agile**: Ongoing (acceptance criteria, automated tests, TDD).
9. **What is the agile testing quadrant?**
    - Agile categorization of tests along two axes:
        - **Technology-Facing** ↔ **Business-Facing**.
        - **Support the Team** ↔ **Critique the Product**.
10. **What is best, from an agile perspective, many manual tests or many automated tests?**
    

- **Automated tests** with minimal manual tests:
    - Faster feedback.
    - Fewer errors.
    - More efficient testing process.

---

### **369: Configuration Management and DevOps**

---

#### **Example Questions**

1. **What is Configuration Management (CM) concerned with?**
    - Managing **policies**, **processes**, and **tools** to handle changes in software systems.
2. **What are the key activities in CM?**
    - **Version Management**: Track versions of software components.
    - **System Building**: Assemble components into executable systems.
    - **Change Management**: Handle change requests.
    - **Release Management**: Prepare and document system releases.
3. **What are CM branching and merging?**
    - Techniques to support releases, builds, and baselines.
4. **What is a baseline?**
    - A description of a release, including:
        - Versions of code files.
        - Documentation.
        - External libraries.
    - Allows rebuilding the release in the future.
5. **What goes into a release?**
    - Code, data, configuration files, and documentation.
6. **What is DevOps, and how can you define it?**
    - DevOps integrates **development** and **operations** to streamline the development and deployment process.
    - Defined by **The Three Ways**: Flow, Feedback, Continuous Learning.
7. **What is the purpose of Continuous Integration (CI)?**
    - Automatically integrates and tests developers' work frequently to identify issues early.
8. **What is the purpose of Continuous Delivery and Deployment?**
    - **Continuous Delivery**: Ensure the code is always deployable.
    - **Continuous Deployment**: Automate deployment for every change, enabling faster and more robust releases.