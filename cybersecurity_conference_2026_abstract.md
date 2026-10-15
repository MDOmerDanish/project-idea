# SpecieHop: Trustless Multi-Hop Decentralized Speculative LLM Inference

Centralized LLM providers impose lock-in, opaque pricing, and single points of failure. In decentralized inference [1], anyone with a spare GPU can sell it, but the provider is untrusted and the client cannot tell what work it pays for. Yet many clients own a laptop, phone, or edge device that can run a small LLM, which enables speculative decoding [2]. We present SpecieHop, a trustless payment system for decentralized speculative LLM inference. The client drafts tokens on its own device, a provider's large model verifies them, and each verification records the work done, so the client pays per accepted token. Speculative state channels settle each round off-chain, though its amount is known only after verification, and a payment-aware KV cache scheduler evicts clients that stop paying.

A channel joins only two parties, so reaching a new provider normally costs a new channel and a locked deposit. Lightning-style routing [3] does not fit: the amount is known only after verification, a hash preimage proves payment but not delivery, and free sessions invite clients to take results and never pay.

SpecieHop routes payments over multiple hops, so a client with one funded channel can pay any provider through untrusted relay Hubs [4]. The provider seals each result under a key that is also the payment secret, so payment and delivery are one event, as in contingent payments [5]. Each hop locks an amount priced by the signed outcome, with a request-price fallback, so every verification is paid for. Per-relay tweaked point locks [6] stop colluding Hubs from skipping an honest relay, and pipelining hides payment latency. Relays never see prompts, and an honest relay never loses funds, even if any set of clients and Hubs deviates arbitrarily.

Our single-hop prototype on a real GPU and live blockchain adds under 1 ms of payment cost per round and is 1.39x faster than autoregressive decoding. For honest traffic, an analytical model shows routed collateral grows linearly with path length, and quadratically only under a stalling Hub, bounded by ledger finality. These multi-hop results come from the model, not yet from measurements. SpecieHop does not prove that inference was computed correctly, and relays learn each batch's accepted count. Next steps are formal security proofs, a simulator, and a three-hop prototype.

**References:**

[1] A. Borzunov, D. Baranchuk, T. Dettmers, M. Ryabinin, Y. Belkada, A. Chumachenko, P. Samygin, and C. Raffel, "Petals: Collaborative inference and fine-tuning of large models," in *Proc. 61st Annu. Meeting Assoc. Computational Linguistics (Volume 3: System Demonstrations)*, Toronto, Canada, Jul. 2023, pp. 558–568.

[2] Y. Leviathan, M. Kalman, and Y. Matias, "Fast inference from transformers via speculative decoding," in *Proc. 40th Int. Conf. Machine Learning (ICML)*, Honolulu, HI, USA, Jul. 2023, ser. Proc. Mach. Learn. Res., vol. 202, pp. 19274–19286.

[3] J. Poon and T. Dryja, "The Bitcoin Lightning Network: Scalable off-chain instant payments," Lightning Network, Tech. Rep., v0.5.9.2, Jan. 2016. [Online]. Available: https://lightning.network/lightning-network-paper.pdf

[4] S. Dziembowski, L. Eckey, S. Faust, and D. Malinowski, "Perun: Virtual payment hubs over cryptocurrencies," in *Proc. IEEE Symp. Security and Privacy (S&P)*, San Francisco, CA, USA, May 2019, pp. 106–123.

[5] M. Campanelli, R. Gennaro, S. Goldfeder, and L. Nizzardo, "Zero-knowledge contingent payments revisited: Attacks and payments for services," in *Proc. ACM SIGSAC Conf. Computer and Communications Security (CCS)*, Dallas, TX, USA, Oct. 2017, pp. 229–243.

[6] G. Malavolta, P. Moreno-Sanchez, C. Schneidewind, A. Kate, and M. Maffei, "Anonymous multi-hop locks for blockchain scalability and interoperability," in *Proc. Network and Distributed System Security Symp. (NDSS)*, San Diego, CA, USA, Feb. 2019.
