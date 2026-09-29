# Cross-Site Request Forgery Protection

Cross-Site Request Forgery (CSRF) exploits a browser that automatically includes a user's credentials, such as cookies, when a malicious page causes a request to another site. A CSRF token is an unpredictable value that the attacker cannot read from the protected origin and therefore cannot easily include in a forged state-changing request.

SameSite cookies and origin checks can add protection, but the exact design depends on the application's authentication model. CSRF protection is mainly relevant when browsers automatically attach ambient credentials.
