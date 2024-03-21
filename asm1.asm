# namename                  
                            
add $1 $2 $zero # begin     
                            
LOOP1: # start              
addi $zero $s1 0x4  # okay      
lw $s1 -0xa($s2)

lui $a2 234

jr $ra

LOOP2:
sw $t1 ($t2)

j END

# now                       
j LOOP1         

        beq $s1 $t1 LOOP2
        sll $1, $23 2

LOOP3:
    bgez $s3 LOOP3

END: