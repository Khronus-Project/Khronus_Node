# Testing Nodes Notes
## Notes
- Band of tolerance in testing demo is only 300 seconds (5 minutes)
- Escenario for testing is the Prototype
- 
# Scenario comparing gas estimations 
## Evening December 22 
- Automated Execution (Estimation by web3 object) - Success 
    - Gas estimated 123,564
    - Gas used 107,282 
- Manual Execution (Estimation by Metamask) - Success
    - Gas estimated 137,881
    - Gas used 121,376 
## Morning December 23
- Automated Execution (Estimation by web3.py)
    - 0xc7970352b0acf3298ed6a8fa06d33b1c3e5bfe33ebf4682c65bcdaca2f935eba - Failed
        - Gas estimated 35,621
        - Gas used 35,480
    - 0xf28f67f9b0bbc1d797b82e16900c491b0845d5c9353d67358acb2c6d1e82f26e - Failed
        - Gas estimated 36,515
        - Gas used 36,360
- Manual Execution (Estimation by Metamask) 
    - 0x9c00717aa20baa7732d5cc6be4aa3287acf87ca9a38db6d9f3bf8e49e88e0a45 - Success
        - Gas estimated 123,564
        - Gas used 107,282
    - 0x7f1b6554e138ca9e0f1729d8179fae81fc6fbf17dfda358584834f9a82e8b55a - Success  
        - Gas estimated 123,552
        - Gas used 107,270
    
## Conclusion
- Issue with gas is related to latency in the network. Need to ensure that gas calculation is performed according to current node.
- If the node has two request that expire in the same minute there will be an issue mostly related to the nonce. 

