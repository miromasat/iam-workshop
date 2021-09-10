import boto3;


ddb = boto3.client('dynamodb', region_name='us-east-1')
ec2 = boto3.client('ec2', region_name='us-east-1')

print("Multi-service test:")
try:
    ec2.describe_instances()
    print("succeeded")
except:
    print("failed")
    
    
print("DDB-table coarse test:")
try:    
    ddb.describe_table(
        TableName='coarse'
    )
    print("succeeded")
except:
    print("failed")    
    
print("DDB-table granular test:")
try:    
    ddb.describe_table(
        TableName='granular'
    )
    print("succeeded")
except:
    print("failed")      

ct = None
gt = None

print("DDB-scan coarse test:")
try:    
    ct = ddb.scan(TableName='coarse')
    print("succeeded")
except:
    print("failed") 
finally:
    print(ct)

print("DDB-scan granular test:")
try:    
    gt = ddb.scan(TableName='granular')
    print("succeeded")
except:
    print("failed") 
finally:
    print(gt)
