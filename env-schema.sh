#Set Bitwarden login name (email address)
EMAIL=

# set 2FA method
#   0: Authenticator
#   1: Email
#   3: YubiKey OTP
MFA_METHOD=

#Set locations to save export files
EXPORT_PATH=

#Set Organization ID (if applicable)
ORG_ID=
#EXAMPLE:   
#org_id="cada13d7-5418-37ed-981b-be822121c593"   
#   To obtain your organization_id value, open a terminal and type:
#   bw login #(follow the prompts); bw list organizations | jq -r '.[0] | .id'
