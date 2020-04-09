	.file	"server.c"
	.section	.rodata
.LC0:
	.string	"ERROR, no port provided\n"
.LC1:
	.string	"sock failed"
.LC2:
	.string	"bind failed"
.LC3:
	.string	"listen failed"
.LC4:
	.string	"accept failed"
.LC5:
	.string	"Connected from %s\n"
.LC6:
	.string	"Connected!!!\n"
.LC7:
	.string	"send failed"
	.text
.globl main
	.type	main, @function
main:
	pushl	%ebp
	movl	%esp, %ebp
	andl	$-16, %esp
	subl	$80, %esp
	cmpl	$1, 8(%ebp)
	jg	.L2
	movl	stderr, %eax
	movl	%eax, %edx
	movl	$.LC0, %eax
	movl	%edx, 12(%esp)
	movl	$24, 8(%esp)
	movl	$1, 4(%esp)
	movl	%eax, (%esp)
	call	fwrite
	movl	$1, (%esp)
	call	exit
.L2:
	movl	12(%ebp), %eax
	addl	$4, %eax
	movl	(%eax), %eax
	movl	%eax, (%esp)
	call	atoi
	movl	%eax, 68(%esp)
	movl	$4, 24(%esp)
	movl	$0, 8(%esp)
	movl	$1, 4(%esp)
	movl	$2, (%esp)
	call	socket
	movl	%eax, 72(%esp)
	cmpl	$-1, 72(%esp)
	jne	.L3
	movl	$.LC1, (%esp)
	call	perror
	movl	$1, (%esp)
	call	exit
.L3:
	movw	$2, 48(%esp)
	movl	68(%esp), %eax
	movzwl	%ax, %eax
	movl	%eax, (%esp)
	call	htons
	movw	%ax, 50(%esp)
	movl	$0, 52(%esp)
	movl	$8, 4(%esp)
	leal	48(%esp), %eax
	addl	$8, %eax
	movl	%eax, (%esp)
	call	bzero
	leal	48(%esp), %eax
	movl	$16, 8(%esp)
	movl	%eax, 4(%esp)
	movl	72(%esp), %eax
	movl	%eax, (%esp)
	call	bind
	cmpl	$-1, %eax
	jne	.L4
	movl	$.LC2, (%esp)
	call	perror
	movl	$1, (%esp)
	call	exit
.L4:
	movl	$10, 4(%esp)
	movl	72(%esp), %eax
	movl	%eax, (%esp)
	call	listen
	cmpl	$-1, %eax
	jne	.L5
	movl	$.LC3, (%esp)
	call	perror
	movl	$1, (%esp)
	call	exit
.L5:
	movl	$16, 28(%esp)
	leal	28(%esp), %edx
	leal	32(%esp), %eax
	movl	%edx, 8(%esp)
	movl	%eax, 4(%esp)
	movl	72(%esp), %eax
	movl	%eax, (%esp)
	call	accept
	movl	%eax, 76(%esp)
	cmpl	$-1, 76(%esp)
	jne	.L6
	movl	$.LC4, (%esp)
	call	perror
	movl	$1, (%esp)
	call	exit
.L6:
	movl	36(%esp), %eax
	movl	%eax, (%esp)
	call	inet_ntoa
	movl	$.LC5, %edx
	movl	%eax, 4(%esp)
	movl	%edx, (%esp)
	call	printf
	movl	$0, 12(%esp)
	movl	$13, 8(%esp)
	movl	$.LC6, 4(%esp)
	movl	76(%esp), %eax
	movl	%eax, (%esp)
	call	send
	cmpl	$-1, %eax
	jne	.L7
	movl	$.LC7, (%esp)
	call	perror
	movl	76(%esp), %eax
	movl	%eax, (%esp)
	call	close
	movl	$1, (%esp)
	call	exit
.L7:
	leal	24(%esp), %eax
	movl	%eax, 8(%esp)
	leal	64(%esp), %eax
	movl	%eax, 4(%esp)
	movl	76(%esp), %eax
	movl	%eax, (%esp)
	call	clientComm
	movl	%eax, (%esp)
	call	free
	jmp	.L7
	.size	main, .-main
	.section	.rodata
.LC8:
	.string	"recv failed"
.LC9:
	.string	"ERROR, no way to print out\n"
	.text
.globl clientComm
	.type	clientComm, @function
clientComm:
	pushl	%ebp
	movl	%esp, %ebp
	subl	$56, %esp
	movl	$0, -12(%ebp)
	movl	16(%ebp), %eax
	movl	%eax, 16(%esp)
	movl	12(%ebp), %eax
	movl	%eax, 12(%esp)
	movl	$7, 8(%esp)
	movl	$1, 4(%esp)
	movl	8(%ebp), %eax
	movl	%eax, (%esp)
	call	getsockopt
	movl	12(%ebp), %eax
	movl	(%eax), %eax
	movl	%eax, (%esp)
	call	malloc
	movl	%eax, -16(%ebp)
	movl	12(%ebp), %eax
	movl	(%eax), %eax
	movl	$0, 12(%esp)
	movl	%eax, 8(%esp)
	movl	-16(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	8(%ebp), %eax
	movl	%eax, (%esp)
	call	recv
	movl	%eax, -12(%ebp)
	cmpl	$-1, -12(%ebp)
	jne	.L10
	movl	$.LC8, (%esp)
	call	perror
	movl	$1, (%esp)
	call	exit
.L10:
	movl	-12(%ebp), %eax
	addl	-16(%ebp), %eax
	movb	$0, (%eax)
	movl	-12(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	-16(%ebp), %eax
	movl	%eax, (%esp)
	call	DataPrint
	testl	%eax, %eax
	je	.L11
	movl	stderr, %eax
	movl	%eax, %edx
	movl	$.LC9, %eax
	movl	%edx, 12(%esp)
	movl	$27, 8(%esp)
	movl	$1, 4(%esp)
	movl	%eax, (%esp)
	call	fwrite
	movl	$1, (%esp)
	call	exit
.L11:
	movl	-16(%ebp), %eax
	movl	%eax, 4(%esp)
	leal	-21(%ebp), %eax
	movl	%eax, (%esp)
	call	strcpy
	leal	-21(%ebp), %eax
	movl	%eax, (%esp)
	call	strlen
	movl	$0, 12(%esp)
	movl	%eax, 8(%esp)
	leal	-21(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	8(%ebp), %eax
	movl	%eax, (%esp)
	call	send
	cmpl	$-1, %eax
	jne	.L12
	movl	$.LC7, (%esp)
	call	perror
	movl	8(%ebp), %eax
	movl	%eax, (%esp)
	call	close
	movl	$1, (%esp)
	call	exit
.L12:
	movl	-16(%ebp), %eax
	leave
	ret
	.size	clientComm, .-clientComm
	.section	.rodata
	.align 4
.LC10:
	.string	"You weren't supposed to get here!"
	.text
.globl secretFunction
	.type	secretFunction, @function
secretFunction:
	pushl	%ebp
	movl	%esp, %ebp
	subl	$24, %esp
	movl	$.LC10, (%esp)
	call	puts
	movl	$1, (%esp)
	call	exit
	.size	secretFunction, .-secretFunction
	.section	.rodata
.LC11:
	.string	"RECEIVED: %s"
.LC12:
	.string	"RECEIVED BYTES: %d\n\n"
	.text
.globl DataPrint
	.type	DataPrint, @function
DataPrint:
	pushl	%ebp
	movl	%esp, %ebp
	subl	$24, %esp
	movl	$.LC11, %eax
	movl	8(%ebp), %edx
	movl	%edx, 4(%esp)
	movl	%eax, (%esp)
	call	printf
	movl	$.LC12, %eax
	movl	12(%ebp), %edx
	movl	%edx, 4(%esp)
	movl	%eax, (%esp)
	call	printf
	movl	$0, %eax
	leave
	ret
	.size	DataPrint, .-DataPrint
	.ident	"GCC: (GNU) 4.4.7 20120313 (Red Hat 4.4.7-23)"
	.section	.note.GNU-stack,"",@progbits
