2.1. Understand the Industry
1. Explain briefly the money flow, the information flow and the role of the main players in
the payment industry.

Answer:

The Money Flow starts with the issuing bank debiting the value of the purchase. Then, the issuing bank repass the value to the acquirer via flag, discouting Its taxes. Then, the acquirer repass the value to the merchant discouting Its own taxes and the cost of the flag, and, the last step, the issuing bank and the acquirer perform the conciliation and liquidation of the transactions.

The Information Flow  begins with the customer starting a transaction (purchase). The information ( card info and values ) are sended by the merchant to the acquirer. Then the acquirer send a solicitation to the card flag. Then, the flag send the solicitation to the issuing bank of the customer's card, and then, the last step is the issuing bank veryfing if the card Is valid and if there are sufficient founds. The answer (approved or denied) follows back the pathing to the merchant.


2. Explain the main differences between acquirer, sub-acquirer and payment gateway, and
how the flow explained in the previous question changes for these players.

Answer:

- Acquirer
  - function:
      - Acredits the merchant to accept payments with cards.
  - Flow:
      - Directly intermediate between the merchant and the flag. It Is responsable for the liquidation (recieving and repass the money) and all the comunication to the network. Like: Cielo and Getnet.
- Sub-acquirer:
  - Function:
      - A intermediate that acredits small and medium merchants between an acquirer. Acts like an "agragator".
  - Flow:
      - The sub-acquirer recieve the money flow of the merchants and repass It to the acquirer like if the transactions belongs to the sub-acquierer, It's responsable by the risk managment, anti-fraud and repass the payment to the merchants, simplifying their operation. Example: PagSeguro and Mercado Pago.

- Payment Gateway:
    - Function:
      - A technology (platform) that allows the merchant to connect to several acquires and sub-acquires. It's like an "roteator" of transactions.
    - Flow:
      - A gateway doesn't deal with the money liquidation. Its only directs the information flow of the transaction to the acquirer or sub-acquirer chosen by the merchant, optimizing the process and offering functionalities. Examples: Pagar.me and Vendi. 
3. Explain what chargebacks are, how they differ from a cancellation and what is their
connection with fraud in the acquiring world.

Answer:

- Chargeback:
  - It's a reversion of the transaction, started by the customer (alegging to the issuing bank that he didn't start the purchase, or the ammount is wrong and etc.) and then the ammount is charged back to him. The acquirer take back the value of the merchant.

- Difference between Chargeback and Cancellation:
  - Cancelation: It's started by the merchant, usually friendly, before the product get shipped or by an agreement with the customer. The merchant gives back the money to the customer.
  - Chargeback: It's started by the customer to the issuing bank, often in a litigious manner, without the conception of the merchant. Its a formal and bureaucratic process, with the participation of the flag bank.

- Conection with fraud:
  - Most of the chargeacks is caused by a not authorized purchase, where the card holder doesn't recognize the transaction.
  - A high rate of chargeacks for a merchant can lead to fines of the flag, and, in some rarely cases, the de-accreditation for the acquirer part. That's why, the acquirer systems, uses antifraud systems to mitigate the risk of chargebacks.
4. What is an anti-fraud and how an acquirer uses it.

Answer:

- A anti-fraud is a system, that uses rules of machine learning and artificial inteligence to analyse transactions in real time and identify the transactions with most probably of beeing fraudulent. Its objective is mitigate the risk of chargebacks and finantical loses.

- How the acquirer uses It
  - The acquirer integrate the antifraud in its platform.
  - Every transaction that goes throw the acquirer is sent to the antifraud system.
  - The antifraud analyzes the transaction with rules and variables (user history of purchases, values of the purchase, geolocation and etc.) and assignment a risk flag.
  - Based on the risk flag, the acquirer can take a decision before approve the transaction.
  
2.2. Solve the problem

A client sends you an email asking for a chargeback status. You check the system, and see that
we have received his defense documents and sent them to the issuer, but the issuer has not
accepted our defense. They claim that the cardholder continued to affirm that she did not
receive the product, and our documents were not sufficient to prove otherwise.

You respond to our client informing that the issuer denied the defense, and the next day he
emails you back, extremely angry and disappointed, claiming the product was delivered and that
this chargeback is not right.
Considering that the chargeback reason is “Product/Service not provided”, what would you do in
this situation?

Answer:

I'd say this

"I understand your frustration with this decision. It's disapointed when we have strong proofs that the product was delivered, and Im sorry that the card issuer had not considered It suficient.

Although the issuer has denied our initial defense, that's not the finish of the process. We still can proceed with an abitration, that is a formal process with the card flag (like Visa or Mastercard). In this case, a third impartial part will revise the case.

To success in this proceed, we need new clearly and convincent evidences. If you can get any of the following itens, we'll be able to build better and stronger proffs.

- A deliverly reciept sign by the card holder.
- Pictures of the product in the deliverly address, provided by the carrier.
- E-mails or messages of the card holder confirming that he got or are using the product.

Please, let us know when you finish It, then we can start imediatly the process of escalonation.

Best regards,

Nicolas"
