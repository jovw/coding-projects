TITLE Program Template     (template.asm)

; Author: Juanette van Wyk
; Last Modified: 19/03/2023
; OSU email address: vanwykj@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number: 6                 Due Date: 19/03/2023
; Description: Program prompt user to enter 10 signed numbers that are smaller than 23 bits. 
;	It read the user input and convert it to a digit. Then display the inputs, calcualte adn display the sum
;	and calcualte and display the average

INCLUDE Irvine32.inc

;--------------------------------------------------------------------------------------------------------
; Name: mGetString
;
; Prompts the user for a value input adn thens tores the value and the size of the value
;
; Receives:
;	[EBP + 8] - prompt
;   [EBP + 20] - userInput 
;   [EBP + 24] - stringSize
;
;--------------------------------------------------------------------------------------------------------
mGetString MACRO prompt, userInput, stringSize
;------------------------------------
; Display Prompt
; Get user Input and stores in memory
;------------------------------------
	push	edx
	push	ecx

	mov		edx, prompt		; display the supplied prompt
	call	WriteString

	mov		edx, userInput
	mov		ecx, stringSize
	call	ReadString

	pop		ecx
	pop		edx
ENDM

;--------------------------------------------------------------------------------------------------------
; Name: mDisplayString
;
; Prints out a string
;
; Receives:
;	String to sprint out
;
;--------------------------------------------------------------------------------------------------------
mDisplayString MACRO string
;------------------------------------
; print string stored in specified memory location
;------------------------------------

	MOV		EDX, string
	CALL	WriteString
 ENDM

 ASCIIZERO = 48
 ASCIININE = 57
 INPUTLIMIT = 10
 ASCIIPLUS = "+"
 ASCIIMINUS = "-"

.data
	program_name			BYTE	"PROGRAMMING ASSIGNMENT 6: Designing low-level I/O procedures", 13,10,0
	my_name					BYTE	"Written by: Juanette van Wyk", 13,10,0
	intro_1					BYTE	"Please provide 10 signed decimal integers.",13,10,0
	intro_2					BYTE	"Each number needs to be small enough to fit inside a 32 bit register.", 13,10 
							BYTE	"After you have finished inputting the raw numbers I will display a", 13,10 
							BYTE	"list of the integers, their sum, and their average value.", 13,10,0
	goodbye					BYTE	"Thanks for playing, have a nice spring break!", 13,10,0
	prompt					BYTE	"Please enter a signed number: ", 0
	error					BYTE	"ERROR: you did not enter a signed number or your number is too big.",13,10,0
	try_again				BYTE	"Please try again: ", 0
	your_inputs_msg			BYTE	"You entered the following numbers:",13,10,0
	comma_sapce				BYTE	", ",0
	sum_value_msg			BYTE	"The sum of these numbers is: ", 0
	avg_value_msg			BYTE	"The truncated average is: ",0
	sum_value				SDWORD	?
	avg_value				SDWORD	?

	numeric_values			SDWORD	INPUTLIMIT DUP(?) ; array to store the converted values
	input					BYTE	255 DUP(0)		  ; to store user string input
	string_value			BYTE	32	DUP(?)		  ; temp storage top print the string


.code
main PROC
;------------------------------------
; Introduction
;------------------------------------
	PUSH	OFFSET		intro_2
	PUSH	OFFSET		intro_1
	PUSH	OFFSET		my_name
	PUSH	OFFSET		program_name
	CALL	introduction

;------------------------------------
; getUserInput
;------------------------------------
	PUSH	OFFSET		numeric_values
	PUSH	SIZEOF		input
	PUSH	OFFSET		input
	PUSH	OFFSET		try_again
	PUSH	OFFSET		error
	PUSH	OFFSET		prompt
	CALL	getUserInput
	CALL	CrLf

;------------------------------------
; Display Input Value
;------------------------------------
	PUSH	OFFSET		comma_sapce
	PUSH	OFFSET		your_inputs_msg
	PUSH	OFFSET		string_value
	PUSH	OFFSET		numeric_values
	CALL	displayInputValues
	CALL	CrLf
	CALL	CrLf

;------------------------------------
; Display Sum value
;------------------------------------
	PUSH	OFFSET		sum_value_msg
	PUSH	OFFSET		sum_value
	PUSH	OFFSET		string_value
	PUSH	OFFSET		numeric_values
	CALL	displaySum
	CALL	CrLf

;------------------------------------
; Display Avg Value
;------------------------------------
	PUSH	OFFSET		avg_value_msg
	PUSH	OFFSET		sum_value
	PUSH	OFFSET		avg_value
	PUSH	OFFSET		string_value
	CALL	displayAvg
	CALL	CrLf
	CALL	CrLf

;------------------------------------
; goodbye
;------------------------------------
	PUSH	OFFSET		goodbye
	CALL	goodbye_proc
  exit
main ENDP

;--------------------------------------------------------------------------------------------------------
; Name: introduction
;
; Prints out program anme, my name, program description and instructions
;
; Receives:
;	[EBP + 8] - prpgram_name
;	[EBP + 12] - my_name
;	[EBP + 16] - intro_1
;	[EBP + 20] - program_name
;
;--------------------------------------------------------------------------------------------------------
introduction PROC
	PUSH	EBP
	MOV		EBP, ESP

	mDisplayString	[EBP + 8]		; print program_name
	mDisplayString	[EBP + 12]		; print my_name
	CALL	CrLf
	mDisplayString	[EBP + 16]		; print intro_1
	mDisplayString	[EBP + 20]		; print intro_2
	CALL	CrLf

	POP		EBP
	RET		16
introduction ENDP

;--------------------------------------------------------------------------------------------------------
; Name: getUserInput
;
; Fills Array with users input in numeric value. Calls on ReadVal to read the user's input value
;
; Postconditions: Numeric values are stored in numeric_values
;	chnages ECX and EDI
;
; Receives:
;	[EBP + 28] - numeric_values
;	[EBP + 24] - sizeof input
;	[EBP + 20] - input
;	[EBP + 16] - try_again
;	[EBP + 12] - error
;	[EBP + 8] - prompt
;
; Returns:
;
;--------------------------------------------------------------------------------------------------------
getUserInput PROC
	PUSH	EBP
	MOV		EBP, ESP
; set up to fill array
	MOV		EDI, [EBP + 28]			; address to numeric_values
	MOV		ECX, INPUTLIMIT			; set limit of array

; fill array loop
_fillArray:
	PUSH	[EBP + 24]				; sizeof input
	PUSH	[EBP + 20]				; input
	PUSH	[EBP + 16]				; try agin
	PUSH	[EBP + 12]				; error
	PUSH	[EBP + 8]				; prompt
	CALL	ReadVal

	ADD		EDI, 4
	LOOP	_fillArray

	POP		EBP
	RET		24
getUserInput ENDP

;--------------------------------------------------------------------------------------------------------
; Name: Read Val
;
; Reads the Input value and converts it to a numeric value
;
; Preconditions:
;	must receive the prompt, error message, try_again message, input address and size_of address from getUserInput
;
; Postconditions:
;	changes: EAX, AL, EDX, ECX, EBX
;	stores EAX in EDI
;
; Receives:
;	[EBP + 24]	- sizeof input
;	[EBP + 20]	- input
;	[EBP + 16]	- try agin
;	[EBP + 12]	- error
;	[EBP + 8]	- prompt
;
; Returns:
;	Stores EAX (converted values) in EDI
;--------------------------------------------------------------------------------------------------------
ReadVal PROC

	; store all registers
	PUSHAD
	PUSH	EDI
	PUSH	ECX

;------------------------------------
; Read user input
;------------------------------------
_readInput:
	mGetString [EBP + 8], [EBP + 20], [EBP + 24]
	MOV		EDX, [EBP + 20]
	MOV		ESI, EDX		; point to first element, set up to LODSB
	MOV		ECX, EAX
	CLD						
	MOV		EAX, 0
	MOV		EBX, 0

;------------------------------------
; Validate user input
;------------------------------------
_validate_string:
	LODSB
	CMP		AL, ASCIIPLUS
	JE		_noError
	CMP		AL,	ASCIIMINUS
	JE		_noError
	CMP		AL,	ASCIIZERO
	JL		_invalidNum
	CMP		AL, ASCIININE
	JG		_invalidNum
	JMP		_convertToNum

_invalidNum:
	mDisplayString	[EBP + 12]
	mGetString [EBP + 16], [EBP + 20], [EBP + 24]
	MOV		EDX, [EBP + 20]
	MOV		ESI, EDX
	MOV		ECX, EAX
	CLD
	MOV		EAX, 0
	MOV		EBX, 0
	JMP		_validate_string

;------------------------------------
; Convert to Num
;------------------------------------
_convertToNum:
	SUB		AL, ASCIIZERO
	XCHG	EAX, EBX
	MOV		EDX, INPUTLIMIT
	MUL		EDX
	JC		_invalidNum
	JNC		_noError
;------------------------------------
; add to accumulator
;------------------------------------
_noError:
	ADD		EAX, EBX
	XCHG	EAX, EBX
	LOOP 	_validate_string

;------------------------------------
; Store in EDI and go back to counter for Array
;------------------------------------
	XCHG	EBX, EAX
	STOSD
	; restore registers
	POP		ECX
	POP		EDI
	POPAD
	RET		20
ReadVal ENDP

;--------------------------------------------------------------------------------------------------------
; Name: displayInputValues
;
; print out array of input values. Call on WriteVal to print value
;
; Preconditions:
;	Numeric values store in Numeric_value array
;
; Postconditions:
;   Changes - EAX, EDX, AL, AX, DX
;
; Receives:
;	 [EBP + 20] - comma_space
;	 [EBP + 16] - your_input_message
;	 [EBP + 12] - string_value
;	 [EBP + 8] - numeric_values
;
;--------------------------------------------------------------------------------------------------------
displayInputValues PROC
	PUSH	EBP
	MOV		EBP, ESP

;------------------------------------
; Display string
;------------------------------------
	mDisplayString	[EBP + 16]

;------------------------------------
; Set up for printing values
;------------------------------------
	MOV		ESI, [EBP + 8]
	MOV		ECX, INPUTLIMIT
	CLD

;------------------------------------
; Loop to display values
;------------------------------------
_displayValues:
	PUSH	[EBP + 12]
	PUSH	ESI
	CALL	WriteVal
	LODSD
	CMP		ECX, 1				; to avoid printing comme after last value
	JE		_lastDigit
	mDisplayString [EBP + 20]

_lastDigit:
	LOOP	_displayValues

	POP		EBP
	RET		16
displayInputValues ENDP

;--------------------------------------------------------------------------------------------------------
; Name: displaySum 
;
; Adds all the values together and then calls on WriteVal to print the value
;
; Preconditions:
;	Array of unput values in numeric_values	
;
; Postconditions:
;	Changes - EBX, EAX, EDX, EDI, AL, BX, DX, AX
;
; Receives:
;	[EBP + 20] - sum_value_msg
;	[EBP + 16] - sum_value
;	[EBP + 12] - string_value
;	[EBP + 8] - numeric_values
;
; Returns: sum value in sume_vlaue
;
;--------------------------------------------------------------------------------------------------------
displaySum	PROC
	PUSH	EBP
	MOV		EBP, ESP
;------------------------------------
; Display string
;------------------------------------
	mDisplayString [EBP + 20]

;------------------------------------
; Set up to write value
;------------------------------------
	MOV		ESI, [EBP + 8]
	MOV		ECX, INPUTLIMIT
	MOV		EBX, 0
	CLD
;------------------------------------
; Loop to sum values
;------------------------------------
_sumLoop:
	LODSD

;------------------------------------
; store values in EAX, ECX, and EBX
; because _getDigit needs to check if a
; negatuve value is present and these values will be needed after
;------------------------------------
	PUSH	EAX
	PUSH	ECX
	PUSH	EBX
;------------------------------------
; set up for _getDigit
;------------------------------------
	MOV		ECX, INPUTLIMIT
	XOR		EBX, EBX
;------------------------------------
; Loop to check is a neg value present
;------------------------------------
_getDigit:
	XOR		EDX, EDX
	DIV		ECX
	PUSH	EDX
	CMP		AL, 45
	JE		_subtract			; if a negative value is present subtract and dont add
	INC		EBX
	CMP	EAX, 0
	JNE		_getDigit	

_popebx:						; pop EDX that was pushed during _getDigit
	POP		EDX
	DEC		EBX
	CMP		EBX, 0
	JNE		_popebx

;------------------------------------
; Restore values for addition
;------------------------------------
	POP		EBX
	POP		ECX
	POP		EAX
	ADD		EAX, EBX
	XCHG	EAX, EBX
	LOOP	_sumLoop
	JMP		_endOfLoop

;------------------------------------
; Subtract 45___ from the digit
; to subtract the correct amount.
; 45 is there to indicate that this is a negative value
; but negatuive should not be part of the subtraction so this 
; is to remove the 45
;------------------------------------
_subtract:	
	MOV		EDI, 45
	MOV		ECX, 10
	INC		EBX
_popedx:
	MUL		ECX
	POP		EDX
	DEC		EBX
	CMP		EBX, 0
	JNE		_popedx

;------------------------------------
; Restore values to subtract
;------------------------------------
	MOV		EDI, EAX
	POP		EBX
	POP		ECX
	POP		EAX
	SUB		EAX, EDI
	SUB		EBX, EAX
	LOOP	_sumLoop
	JMP		_endOfLoop

;------------------------------------
; Set up to call WriteVal
;------------------------------------
_endOfLoop:
	XCHG	EAX, EBX
	MOV		EDI, [EBP + 16]
	MOV		[EDI], EAX
	PUSH	[EBP + 12]
	PUSH	EDI
	CALL	WriteVal

	POP		EBP
	RET		16
displaySum ENDP

;--------------------------------------------------------------------------------------------------------
; Name: displayAvg
;
; Calculated the truncated avg and calls to WrtieVal to display
;
; Preconditions:
;	Sum has to be calculated
;
; Postconditions:
;	changes: EBX, EAX, EDX, EDI
;
; Receives:
;	[EBP + 20] - avg_value_msg
;	[EBP + 16] - sum_value
;	[EBP + 12] - avg_value
;	[EBP + 8] - string_value
;
; Returns: avg value in avg_value
;
;--------------------------------------------------------------------------------------------------------
displayAvg PROC
	PUSH	EBP
	MOV		EBP, ESP
;------------------------------------
; Display string
;------------------------------------
	mDisplayString	[EBP + 20]

;------------------------------------
; Set up to subtract
;------------------------------------
	MOV		EDI, [EBP +16]
	MOV		EAX, [EDI]
	MOV		EBX, INPUTLIMIT
	CDQ
	IDIV	EBX

;------------------------------------
; Set up to call WriteVal
;------------------------------------
	MOV		EDI, [EBP + 8]
	MOV		[EDI], EAX
	PUSH	[EBP + 12]
	PUSH	EDI
	CALL	WriteVal

	POP		EBP
	RET		16
displayAvg ENDP

;--------------------------------------------------------------------------------------------------------
; Name: WriteVal
;
; Converts the ASCII value into a digit to print
;
; Preconditions:
;	have to have a value to convert
;	have to have a array address to store the value in
;
; Receives:
;	address for string_value
;	value to be written
;
;--------------------------------------------------------------------------------------------------------
WriteVal PROC
	PUSH	EBP
	MOV		EBP, ESP
	PUSHAD

	MOV		EDI, [EBP + 8]		; moves value to write
	MOV		EAX, [EDI]
	MOV		ECX, INPUTLIMIT	
	XOR		BX, BX				; clear EBX

;------------------------------------
; Loop to get each digit in the string
;------------------------------------
_getDigit:
	XOR		EDX, EDX
	CMP		AL, 45
	JE		_sign				; jump if sign
	CMP		AL, 43
	JE		_sign

	XOR		EDX, EDX			; clear EDX
	DIV		ECX
	PUSH	DX					; store the digit
	INC		BX
	CMP		EAX, 0
	JNE		_getDigit

	MOV		ESI, [EBP + 12]		
	MOV		CX, BX
	JMP		_conversionLoop

;------------------------------------
; Handeling a sign
;------------------------------------
_sign:							
	MOV		DX, AX
	PUSH	DX
	MOV		ESI, [EBP + 12]
	MOV		CX, BX
	JMP		_conversionLoop

;------------------------------------
; Convert the digit and then print each digit
;------------------------------------
_conversionLoop:
	POP		AX
	CMP		AX, ASCIIPLUS
	JE		_conversionLoop		; skip printing the +
	CMP		AX, ASCIIMINUS
	JE		_convertSign

	ADD		AX, ASCIIZERO
	MOV		[ESI], AX
	mDisplayString ESI
	LOOP	_conversionLoop
	JMP		_done

_convertSign:
	MOV		[ESI], AX
	mDisplayString ESI
	JMP		_conversionLoop

_done:
	MOV		EDX, 0
	POPAD
	POP		EBP
	RET		8
WriteVal ENDP

;--------------------------------------------------------------------------------------------------------
; Name: goodbye_proc
;
; Prints farewell message
;
; Receives:
;	[EBP + 8] farewell_msg
;
;--------------------------------------------------------------------------------------------------------
goodbye_proc PROC
	PUSH	EBP
	MOV		EBP, ESP
	mDisplayString	[EBP + 8]

	POP		EBP
	RET		4
goodbye_proc ENDP

END main





