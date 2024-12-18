# Backend system that takes in contracts and compares to ERP data.

The system is designed to provide:

1. Document Question and Answer
    This works pretty well currently, with an example being run for the following questions in app.py:
        - What is the item being delivered?
        - When is it being delivered?
        - How much of the item is being delivered?
        - Are there any late delivery clauses?
        - Are there any other clauses that incur financial penalties?

    The responses generated seemed reasonable and fairly accurate.

2. Database Retrieval and Breach Detection
    I have struggled a little bit with this, primarily due to my interfacing with the contracts not being standardised enough. This meant I struggled to get a consistent response in a JSON format that allowed me to query the database effectively. A potential way around this would be to get the contract ID from the contract, look up the deliverables, and then input that as a prompt to the LLM along with the contract again to check if the requirements had been met. I think this would be more likely to work; however, I wanted to move on to the final requirement and hence did not get to this.

    I focused mainly on the factors in the database that I know to differ between the example contracts I was given. For instance, retrieving values such as the delivery date or pallet size, which could then be directly compared to the database by filtering by contract number and joining the deliveries and items views. These comparisons are then fed into an LLM, which provides an output indicating whether the contract has been breached, stating which areas have not been met and highlighting where the system could not find the correct value in the contract, requiring human intervention.

3. Action Tracking
    I was able to create a system that fairly nicely applies annotations to the contract, outputting a .html version of the contract with highlights. There are current issues where the structured response from the LLM, which contains the locations of the data used in database retrieval, does not align accurately with the document. Again, I ran out of time to engineer the system to work better. It seems more reliable with some data, such as the contract number, which is commonly at the start of the document, so perhaps it is an issue with the technique I was using.

Other Features
    I added some caching to the system. This hashes the message sent to the LLM and stores the response so that if the same message is asked again, it can provide the local response. This was primarily to reduce costs, both in terms of time and money, as the response from OpenAI for the fairly long reads was far from instant.

Additional Features Not Yet Implemented
    I did not have time to push all data to an SQL database or deploy the system to the cloud. I made some progress on structuring my LLM outputs, but I would not say it is perfect yet!

Running app.py from the contract_breach_detector directory within a venv that has the libraries installed from requirements.txt should provide an example of the three tasks above. In case there are any unforeseen issues, I would expect an output that looks like the below:

```
$ python app.py
        -----------------------------------------------
        Copper_contract
        Responses to Example Questions:
        Q: What is the item being delivered
        A: 1 cm diameter coated copper cable
        Q: When is it being delivered
        A: June 15th 2024
        Q: How much of the item is being delivered
        A: 1 reel
        Q: Are there any late delivery clauses
        A: If the Goods are not delivered on the relevant Delivery Date, the Customer may claim or deduct 10% of the price of the Goods for each week's delay in delivery until the earlier of delivery or termination or abandonment of the Contract, up to a maximum of 50% of the total price of the Goods.
        Q: Are there any other clauses that incur financial penalties
        A: The Customer will charge the Supplier storage costs for rejected Goods if they are not collected within a reasonable period after notification of the rejection.

        Contract vs Delivered Comparisons:
        1. The contract states that the value for delivery_date should be 2024-06-15. The delivered value was 2023-12-16 00:00:00.
        2. The contract states that the value for pallet_dimensions should be . The delivered value was 1200mm x 1000mm x 150mm.
        3. The contract states that the value for quantity should be 1 reel. The delivered value was 1.
        4. The contract states that the value for weight should be . The delivered value was 50.0.

        The contract has been breached: The contract has missing values for pallet_dimensions and weight, which constitutes a breach of contract. Human clarification is required.

        An HTML file with highlighted contract information can be found here: /home/oren/Documents/Python/magentic_poc/contract_breach_detector/contracts/highlighted/Copper_contract.html

        -----------------------------------------------
        Steel_contract
        Responses to Example Questions:
        Q: What is the item being delivered
        A: 80 tons of steel reinforcement bars
        Q: When is it being delivered
        A: November 20, 2023
        Q: How much of the item is being delivered
        A: 80 tons
        Q: Are there any late delivery clauses
        A: Yes, the Supplier shall pay liquidated damages at a rate of 1% of the Contract Price for each calendar day of delay, up to a maximum of 15% of the Contract Price.
        Q: Are there any other clauses that incur financial penalties
        A: Yes, underweight deliveries may result in a proportional reduction of the Contract Price.

        Contract vs Delivered Comparisons:
        1. The contract states that the value for delivery_date should be 2023-11-20. The delivered value was 2023-10-20 00:00:00.
        2. The contract states that the value for pallet_dimensions should be Not specified. The delivered value was 1200mm x 1000mm x 150mm.
        3. The contract states that the value for quantity should be 80 tons. The delivered value was 73.
        4. The contract states that the value for weight should be 80 tons. The delivered value was 73000.0.

        The contract has been breached: The delivery_date is early, the pallet_dimensions exceed contract specifications, and the quantity delivered is less than contracted, indicating a breach. Human clarification is required for the discrepancies.

        An HTML file with highlighted contract information can be found here: /home/oren/Documents/Python/magentic_poc/contract_breach_detector/contracts/highlighted/Steel_contract.html

        -----------------------------------------------
        Aluminium_contract
        Responses to Example Questions:
        Q: What is the item being delivered
        A: 500 units of high-grade aluminum sheets
        Q: When is it being delivered
        A: November 16, 2024
        Q: How much of the item is being delivered
        A: 500 units
        Q: Are there any late delivery clauses
        A: Yes, late delivery may incur a penalty of 1% of the contract price for each day of delay, up to a maximum of 15% of the contract price.
        Q: Are there any other clauses that incur financial penalties
        A: Yes, failure to comply with packaging requirements incurs a penalty of $5,000.

        Contract vs Delivered Comparisons:
        1. The contract states that the value for delivery_date should be 2024-11-16. The delivered value was 2023-11-15 00:00:00.
        2. The contract states that the value for pallet_dimensions should be 1200mm x 1000mm x 150mm. The delivered value was 1100mm x 900mm x 130mm.
        3. The contract states that the value for quantity should be 500 units. The delivered value was 500.
        4. The contract states that the value for weight should be Not specified. The delivered value was 10.0.

        The contract has been breached: The delivery date was delivered early, which is acceptable; however, pallet dimensions do not meet the contract specifications, and the weight was not specified in the contract but a value was delivered, indicating a breach.

        An HTML file with highlighted contract information can be found here: /home/oren/Documents/Python/magentic_poc/contract_breach_detector/contracts/highlighted/Aluminium_contract.html

        -----------------------------------------------
        ```