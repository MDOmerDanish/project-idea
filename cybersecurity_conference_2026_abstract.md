# SpecieHop: Trustless Multi-Hop Decentralized Speculative LLM Inference

Centralized LLM providers impose lock-in, opaque pricing, and single points of failure. Decentralized inference [1] lets anyone with a spare GPU sell compute, but the provider is untrusted and the client cannot verify what work it pays for. Many clients, however, own a laptop, phone, or edge device that can run a small LLM, which enables speculative decoding [2]. We present SpecieHop, a trustless payment system for decentralized speculative LLM inference. The client drafts tokens on its own device, a provider's large model verifies them, and each verification records the work done, so the client pays per accepted token. Speculative state channels settle each round off-chain, and a payment-aware KV cache scheduler evicts clients that stop paying.

The central challenge is fairness when both parties may be dishonest: a client must not obtain results without paying, and a provider must not be paid without delivering. This is harder still with untrusted intermediaries between the client and serving Hub. Lightning-style routing [3] does not apply directly, because the amount is known only after verification and a hash preimage proves payment, not delivery.

SpecieHop routes payments over multiple hops, so a client with one funded channel can pay any provider through untrusted relay Hubs [4]. The provider seals each result under a key that is also the payment secret, so payment and delivery form one event, as in contingent payments [5]. Each hop locks an amount priced by the signed outcome, with a request-price fallback, so every verification is paid. Per-relay tweaked point locks [6] prevent colluding Hubs from skipping an honest relay, and pipelining hides payment latency. Relays never see prompts. Even if any clients and Hubs deviate arbitrarily, a client pays only for results it can unlock, the serving Hub receives at least the request price per verification, and an honest relay never loses funds.

Our single-hop prototype, on a real GPU and live blockchain, adds under 1 ms of payment cost per round and is 1.39x faster than autoregressive decoding. For honest traffic, an analytical model shows that routed collateral grows linearly with path length, and quadratically only under a stalling Hub, bounded by ledger finality. These multi-hop results are modeled, not yet measured. SpecieHop does not prove inference correctness, and relays learn each batch's accepted count. Future work includes formal proofs, a simulator, and a three-hop prototype.

**References:**

[1] A. Borzunov, D. Baranchuk, T. Dettmers, M. Ryabinin, Y. Belkada, A. Chumachenko, P. Samygin, and C. Raffel, "Petals: Collaborative inference and fine-tuning of large models," in *Proc. 61st Annu. Meeting Assoc. Computational Linguistics (Volume 3: System Demonstrations)*, Toronto, Canada, Jul. 2023, pp. 558–568.

[2] Y. Leviathan, M. Kalman, and Y. Matias, "Fast inference from transformers via speculative decoding," in *Proc. 40th Int. Conf. Machine Learning (ICML)*, Honolulu, HI, USA, Jul. 2023, ser. Proc. Mach. Learn. Res., vol. 202, pp. 19274–19286.

[3] J. Poon and T. Dryja, "The Bitcoin Lightning Network: Scalable off-chain instant payments," Lightning Network, Tech. Rep., v0.5.9.2, Jan. 2016. [Online]. Available: https://lightning.network/lightning-network-paper.pdf

[4] S. Dziembowski, L. Eckey, S. Faust, and D. Malinowski, "Perun: Virtual payment hubs over cryptocurrencies," in *Proc. IEEE Symp. Security and Privacy (S&P)*, San Francisco, CA, USA, May 2019, pp. 106–123.

[5] M. Campanelli, R. Gennaro, S. Goldfeder, and L. Nizzardo, "Zero-knowledge contingent payments revisited: Attacks and payments for services," in *Proc. ACM SIGSAC Conf. Computer and Communications Security (CCS)*, Dallas, TX, USA, Oct. 2017, pp. 229–243.

[6] G. Malavolta, P. Moreno-Sanchez, C. Schneidewind, A. Kate, and M. Maffei, "Anonymous multi-hop locks for blockchain scalability and interoperability," in *Proc. Network and Distributed System Security Symp. (NDSS)*, San Diego, CA, USA, Feb. 2019.
