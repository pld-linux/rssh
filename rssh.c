/*
 * rssh.c - restricted shell for ssh to allow scp or sftp only
 * 
 * Copyright 2002 Derek D. Martin <ddm@pizzashack.org>.
 *
 * This program is licensed under a BSD-style license, as follows: 
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */

#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <libgen.h>
#include <wordexp.h>

/* for sftp */
#define _PATH_SFTP_SERVER       "/usr/libexec/openssh/sftp-server"

#define _ALLOW_SCP 1
#define _ALLOW_SFTP (1 << 1)

void do_exit_message( int flags );
char **build_arg_vector( char *str );

extern int errno;

int main( int argc, char **argv )
{

    char **argvec;
    int  allowed_command = 0;
    int  flag = 0;

    /*  check argv[0] for scp or sftp to see what's allowed */
    if ( !strcmp(basename(argv[0]), "scpsh") ) 
        allowed_command = _ALLOW_SCP;
    if ( !strcmp(basename(argv[0]), "sftpsh") )
        allowed_command = _ALLOW_SFTP;
    if ( !strcmp(basename(argv[0]), "rssh") ) 
        allowed_command = _ALLOW_SFTP | _ALLOW_SCP;

    /* q&d arg count check */
    if ( argc < 3 ) do_exit_message(allowed_command);

    /* if first arg is anything but -c, it's no good */
    if ( strcmp("-c", argv[1]) ) do_exit_message(allowed_command);

    /* convert argv[2] into an arg vector suitable for execvp() */
    argvec = build_arg_vector(argv[2]);

    /* check to see if we got an allowed command */
    if ( (!strcmp(argvec[0], _PATH_SFTP_SERVER)) && 
        (allowed_command & _ALLOW_SFTP ) )
        flag = 1;
    if ( (!strcmp(argvec[0], "scp") && (allowed_command & _ALLOW_SCP)) )
        flag = 1;

    /* if no allowed command, print message and exit */
    if ( !flag )
        do_exit_message(allowed_command);

    /* if all that passed, exec the relevant command */
    execvp(argvec[0], argvec);

    /* we only get here if the exec fails */
    fprintf(stderr, "rssh: excecvp() failed.  ");

    switch (errno){

        case EACCES:
        case ENOTDIR:
        case ENOENT:
            fprintf(stderr, "%s is not an executable file, or permission denied.\n\n", argv[2]);
            break;
        case EPERM:
            fprintf(stderr, "FS mounted nosuid or process is being traced\n"
                    "(and you are not root)\n\n");
            break;
        default:
            fprintf(stderr, "an unknown error occurred.\n\n");
    }
    
    exit(1);
}


char **build_arg_vector( char *str )
{

    wordexp_t   result;

    if ( (wordexp(str, &result, 0)) ){
        fprintf(stderr, "rssh: error expanding arguments\n");
        exit(1);
    }

    return result.we_wordv;
}


void do_exit_message( int flags )
{

    if ( !flags ){
        fprintf(stderr, "\nrssh is not installed correctly!  Your sysadmin"
                " is on crack!\n");
        exit(1);
    }

    fprintf( stderr, "\nThis account is restricted, for the use of ");

    switch (flags){
        case (_ALLOW_SCP | _ALLOW_SFTP):
            fprintf(stderr, "scp or sftp");
            break;
        case _ALLOW_SCP:
            fprintf(stderr, "scp");
            break;
        case _ALLOW_SFTP:
            fprintf(stderr, "sftp");
            break;
        default:
            fprintf(stderr, "\n\nrssh error!  This can only happen if rssh"
                    " is not installed correctly.\n  Please see your "
                    "system administrator.\n\n");
    }

    fprintf(stderr, " only.\nIf you believe this is in error, please contact"
             " your system\nadministrator.\n\n" );
    exit(0);
}


