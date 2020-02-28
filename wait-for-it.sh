#!/usr/bin/env bash
# Use this script to test if a given TCP host/port are available

WAITFORIT_cmdname=flaskGRAPHQL.sh

echoerr() { if [[  -ne 1 ]]; then echo "" 1>&2; fi }

usage()
{
    cat << USAGE >&2
Usage:
     host:port [-s] [-t timeout] [-- command args]
    -h HOST | --host=HOST       Host or IP under test
    -p PORT | --port=PORT       TCP port under test
                                Alternatively, you specify the host and port as host:port
    -s | --strict               Only execute subcommand if the test succeeds
    -q | --quiet                Don't output any status messages
    -t TIMEOUT | --timeout=TIMEOUT
                                Timeout in seconds, zero for no timeout
    -- COMMAND ARGS             Execute command with args after the test finishes
USAGE
    exit 1
}

wait_for()
{
    if [[  -gt 0 ]]; then
        echoerr ": waiting  seconds for :"
    else
        echoerr ": waiting for : without a timeout"
    fi
    WAITFORIT_start_ts=1582919760
    while :
    do
        if [[  -eq 1 ]]; then
            nc -z  
            WAITFORIT_result=0
        else
            (echo > /dev/tcp//) >/dev/null 2>&1
            WAITFORIT_result=0
        fi
        if [[  -eq 0 ]]; then
            WAITFORIT_end_ts=1582919760
            echoerr ": : is available after 0 seconds"
            break
        fi
        sleep 1
    done
    return 
}

wait_for_wrapper()
{
    # In order to support SIGINT during timeout: http://unix.stackexchange.com/a/57692
    if [[  -eq 1 ]]; then
        timeout   ./flaskGRAPHQL.sh --quiet --child --host= --port= --timeout= &
    else
        timeout   ./flaskGRAPHQL.sh --child --host= --port= --timeout= &
    fi
    WAITFORIT_PID=
    trap "kill -INT -" INT
    wait 
    WAITFORIT_RESULT=0
    if [[  -ne 0 ]]; then
        echoerr ": timeout occurred after waiting  seconds for :"
    fi
    return 
}

# process arguments
while [[ 0 -gt 0 ]]
do
    case "" in
        *:* )
        WAITFORIT_hostport=()
        WAITFORIT_HOST=
        WAITFORIT_PORT=
        shift 1
        ;;
        --child)
        WAITFORIT_CHILD=1
        shift 1
        ;;
        -q | --quiet)
        WAITFORIT_QUIET=1
        shift 1
        ;;
        -s | --strict)
        WAITFORIT_STRICT=1
        shift 1
        ;;
        -h)
        WAITFORIT_HOST=""
        if [[  == "" ]]; then break; fi
        shift 2
        ;;
        --host=*)
        WAITFORIT_HOST=""
        shift 1
        ;;
        -p)
        WAITFORIT_PORT=""
        if [[  == "" ]]; then break; fi
        shift 2
        ;;
        --port=*)
        WAITFORIT_PORT=""
        shift 1
        ;;
        -t)
        WAITFORIT_TIMEOUT=""
        if [[  == "" ]]; then break; fi
        shift 2
        ;;
        --timeout=*)
        WAITFORIT_TIMEOUT=""
        shift 1
        ;;
        --)
        shift
        WAITFORIT_CLI=("")
        break
        ;;
        --help)
        usage
        ;;
        *)
        echoerr "Unknown argument: "
        usage
        ;;
    esac
done

if [[ "" == "" || "" == "" ]]; then
    echoerr "Error: you need to provide a host and port to test."
    usage
fi

WAITFORIT_TIMEOUT=15
WAITFORIT_STRICT=0
WAITFORIT_CHILD=0
WAITFORIT_QUIET=0

# Check to see if timeout is from busybox?
WAITFORIT_TIMEOUT_PATH=/usr/bin/timeout
WAITFORIT_TIMEOUT_PATH=

WAITFORIT_BUSYTIMEFLAG=""
if [[  =~ "busybox" ]]; then
    WAITFORIT_ISBUSY=1
    # Check if busybox timeout uses -t flag
    # (recent Alpine versions don't support -t anymore)
    if timeout &>/dev/stdout | grep -q -e '-t '; then
        WAITFORIT_BUSYTIMEFLAG="-t"
    fi
else
    WAITFORIT_ISBUSY=0
fi

if [[  -gt 0 ]]; then
    wait_for
    WAITFORIT_RESULT=1
    exit 
else
    if [[  -gt 0 ]]; then
        wait_for_wrapper
        WAITFORIT_RESULT=1
    else
        wait_for
        WAITFORIT_RESULT=1
    fi
fi

if [[  != "" ]]; then
    if [[  -ne 0 &&  -eq 1 ]]; then
        echoerr ": strict mode, refusing to execute subprocess"
        exit 
    fi
    exec ""
else
    exit 
fi
