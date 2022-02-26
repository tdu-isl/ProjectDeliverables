
#######################################
# 機能: 出力に色付ける
# 引数:
#   -n: 改行しない
#   -p: [INFO]などのprefixを出力しない
#   $1: 色コード(0~255) or キーワード
#   $2: 出力となる文字列
# 出力:
#   色付き文字列
#######################################
function color_print() {
    OPTIND=0
    declare -r esc=$(printf "\033")    # 色付けるためのprefix
    declare -r reset="${esc}[0m"       # 色、フォント設定をリセット
    declare new_line='true'
    declare no_prefix='false'

    declare option
    while getopts :np option; do
        case $option in
            n)  new_line='false' ;;
            p)  no_prefix='true' ;;
            *)  echo 'error in function color_print'; exit 1; ;;
        esac
    done
    shift $((OPTIND - 1))

    if [[ $# == 0 ]] || [[ $# == 1 && ! -p /dev/stdin ]]; then
        echo "${esc}[1;38;5;9m[Error] 引数ERROR. Usage: color_print 色 文字列${esc}[m"
        exit 1;
    fi

    if [[ -p /dev/stdin ]]; then        # <-- make pipe work
        declare -r str=$(cat -)        # <-- make pipe work
    else
        declare -r str="$2"
    fi

    declare prefix=''
    declare color=''
    case $1 in
    'info')     # blue
        color=33; prefix='[INFO] '; ;;
    'warn')     # yello
        color=190; prefix='[WARN] '; ;;
    'success')  # green
        color=46; prefix='[OK] '; ;;
    'error')    # red
        color=196; prefix='[ERROR] '; ;;
    'tip')      # orange
        color=215; prefix='[TIP] '; ;;
    'debug')
        color=141; prefix='[debug] '; ;;
    *)
        color=$1; ;;
    esac

    if [[ $no_prefix == 'true' ]]; then prefix=''; fi
    if [[ $new_line == 'true' ]]; then
        echo "${esc}[38;5;${color}m${prefix}${str}${reset}"
    else
        echo -n "${esc}[38;5;${color}m${prefix}${str}${reset}"
    fi
    OPTIND=0
}

#######################################
# 機能: カウントダウン(デフォルトは数字を使う)
# 引数:
#   -d: 数字の代わりに . を使う
#   $1: 秒
# 出力:
#   3 2 1 0  または  ....
#######################################
function count_down() {
    OPTIND=0
    declare use_dot='false'
    declare option
    while getopts :d option; do
        case $option in
            d)  use_dot='true' ;;
            *)  echo 'error in function count_down'; exit 1; ;;
        esac
    done
    shift $((OPTIND - 1))

    declare i
    if [[ $use_dot == 'true' ]]; then
        for i in $(seq $1 -1 1); do
            color_print -n 102 '.'
            sleep 1
        done
        echo ''
    else
        for i in $(seq $1 -1 1); do
            echo -n "$i " | color_print -n 102
            sleep 1
        done
        color_print 102 '0'
    fi
    OPTIND=0
}

#######################################
# 機能: Windowと同じ幅の分割線を出力する
# 引数:
#   $1: 分割線用の、1文字。省略すると = を使う
# 出力:
#   ============== など
#######################################
function print_divider() {
    if [[ $# == 0 ]]; then
        eval "printf '%.0s'= {1..$(tput cols)}"
    else
        eval "printf '%.0s'$1 {1..$((  $(tput cols) / ${#1}  ))}"
    fi
    echo ''
}

#######################################
# 機能: yes / no
# 引数:
#   $1: 色コード(0~255) or キーワード
#   $2: メッセージ
# 戻り値:
#   `yes` / `no`   グローバル変数answerに保存
#######################################
function yes_or_no() {
    answer=''
    PS3='数字を選んでください> '
    while true; do
        color_print $1 "$2"
        select answer in yes no; do break; done
        if [[ ${#answer} == 0 ]]; then
            color_print error '正しい数字を選んでください!!!'
            continue
        fi
        return 0
    done
}

#######################################
# 機能: 複数の選択肢から１つ選択(事前にグローバル変数arrayにセット)
# 引数:
#   $1: 色コード(0~255) or キーワード
#   $2: メッセージ
# 戻り値:
#   選ばれた選択肢   グローバル変数answerに保存
#######################################
function select_one() {
    answer=''
    PS3='数字を選んでください> '
    color_print $1 "$2"
    while true; do
        select answer in ${array[@]}; do break; done
        if [[ ${#answer} == 0 ]]; then
            color_print error '正しい数字を選んでください!!!'
            continue
        fi
        return 0
    done
}

#######################################
# 機能: 実行されたスクリプトのディレクトリの絶対パス
# 出力:
#   ディレクトリの絶対パス
#######################################
function get_current_script_dir() {
    declare -r current_path=$(pwd)
    declare -r current_script_dir=$(cd $(dirname $0); pwd)
    cd $current_path
    echo $current_script_dir
}

#######################################
# 機能: readコマンドをラップする
# 引数:
#   $1: 色コード(0~255) or キーワード
#   $2: メッセージ
#   $3: (省略可能)色コード(0~255) or キーワード
#   $4: (省略可能)メッセージ
# 戻り値:
#   ユーザの入力   グローバル変数answerに保存
#######################################
function read_line() {
    answer=''
    color_print $1 "$2"
    if [[ $# == 4 ]]; then
        color_print $3 "$4"
    fi
    while true; do
        read -p '> ' answer
        if [[ ${#answer} == 0 ]]; then
            color_print error '入力は空です!'
            continue
        fi
        break
    done
}
