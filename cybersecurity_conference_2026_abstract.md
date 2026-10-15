# SpecieHop: Trustless Multi-Hop Decentralized Speculative LLM Inference

Centralized LLM providers impose lock-in, opaque pricing, and single points of failure. Decentralized inference [1] lets anyone with a spare GPU sell compute, but the provider is untrusted and the client cannot verify what work it pays for. Many clients own a device that can run a small LLM, enabling speculative decoding [2]. A client may reach the provider directly or through several untrusted hops. We present SpecieHop, a trustless payment system for decentralized speculative LLM inference. The client drafts tokens, a provider's large model verifies them, and each verification records the work done, so the client pays per accepted token. Speculative state channels settle each round off-chain, and a payment-aware KV cache scheduler evicts clients that stop paying.

The core challenge is fairness when both parties may be dishonest: a client must not obtain results without paying, and a provider must not be paid without delivering. Untrusted hops make this harder still. Lightning-style routing [3] does not apply directly, because the amount is known only after verification and a hash preimage proves payment, not delivery.

SpecieHop routes payments over multiple hops, so a client with one funded channel can pay any provider through untrusted relay Hubs [4]. The provider seals each result under a key that is also the payment secret, so payment and delivery form one event [5]. Each hop locks an amount priced by the signed outcome. Per-relay tweaked point locks [6] prevent colluding Hubs from skipping an honest relay. Relays never see prompts. Even if clients and Hubs deviate arbitrarily, a client pays only for results it can unlock, the serving Hub receives at least the request price, and an honest relay never loses funds.

Our single-hop prototype on a real GPU and live blockchain adds under 1 ms of payment cost per round and is 1.39x faster than autoregressive decoding. For honest traffic, an analytical model shows routed collateral grows linearly with path length, and quadratically only under a stalling Hub. These multi-hop results are modeled, not yet measured. SpecieHop does not prove inference correctness, and relays learn each batch's accepted count. Future work: formal proofs, a simulator, a three-hop prototype.

**References:**

[1] A. Borzunov et al., "Petals: Collaborative inference and fine-tuning of large models," in *Proc. ACL (System Demonstrations)*, 2023, pp. 558–568.  
[2] Y. Leviathan, M. Kalman, and Y. Matias, "Fast inference from transformers via speculative decoding," in *Proc. ICML*, 2023, pp. 19274–19286.  
[3] J. Poon and T. Dryja, "The Bitcoin Lightning Network: Scalable off-chain instant payments," Tech. Rep., 2016.  
[4] S. Dziembowski, L. Eckey, S. Faust, and D. Malinowski, "Perun: Virtual payment hubs over cryptocurrencies," in *Proc. IEEE S&P*, 2019, pp. 106–123.  
[5] M. Campanelli et al., "Zero-knowledge contingent payments revisited: Attacks and payments for services," in *Proc. ACM CCS*, 2017, pp. 229–243.  
[6] G. Malavolta et al., "Anonymous multi-hop locks for blockchain scalability and interoperability," in *Proc. NDSS*, 2019.
