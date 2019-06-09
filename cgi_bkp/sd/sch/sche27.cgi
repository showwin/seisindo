#!/usr/bin/perl
if ($ENV{'HTTP_X_FORWARDED_FOR'} =~ /[12]?\d{1,2}(\.[12]?\d{1,2}){3}$/) {
   $ENV{'REMOTE_ADDR'} = $&;
}
$ENV{'REMOTE_HOST'} =
  gethostbyaddr(pack('C4', split('\.',  $ENV{'REMOTE_ADDR'})), 2)
      unless ($ENV{'REMOTE_HOST'});

###############################################
#   sche27.cgi
#      V1.4 (2004.4.26)
#                     Copyright(C) CGI-design
###############################################

$script = 'sche27.cgi';
$base = './schedata';				#�f�[�^�i�[�f�B���N�g��
$nofile = "$base/no.txt";			#�����ݔԍ�
$opfile = "$base/option.txt";		#�I�v�V�����t�@�C��
$lockfile = "$base/lock";			#���b�N
$catmax = 24;						#�ő啶���F��X2

@mdays = (31,28,31,30,31,30,31,31,30,31,30,31);
@week = ('��','��','��','��','��','��','�y');
@wcolor = ("#ff0000","#000000","#000000","#000000","#000000","#000000","#0000ff");

open (IN,"$opfile") || &error("OPEN ERROR");		$opdata = <IN>;		close IN;
if (!$opdata) {
	$pass = &crypt('cgi');
	chmod(0666,$opfile);	open (OUT,">$opfile") || &error("OPEN ERROR");
	print OUT "�X�P�W���[��<>$pass<>http://merlion.cool.ne.jp/cgi/<>$base/home.gif<>$base/back.gif<>$base/next.gif<><>$base/style.css<>#ffffff<>#800000<>#000000<>�R�����g<>6<>#000000<>#FEF5DA<>�ō���<>#000000<>���s<>#0000ff";
	close OUT;
	chmod(0666,$nofile);
}

##### ���C������ #####
if ($ENV{'REQUEST_METHOD'} eq "POST") {read(STDIN,$in,$ENV{'CONTENT_LENGTH'});} else {$in = $ENV{'QUERY_STRING'};}
@pair = split(/&/,$in);
foreach (@pair) {
	($n,$val) = split(/=/);
	$val =~ tr/+/ /;
	$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$val =~ s/&/&amp;/g; $val =~ s/</&lt;/g; $val =~ s/>/&gt;/g; $val =~ s/"/&quot;/g;
	$in{$n} = $val;
}
$mode = $in{'mode'};
$act = $in{'act'};
$wrt = $in{'wrt'};
$logyear = $in{'year'};
$logmon = $in{'mon'};

open (IN, "$opfile") || &error("OPEN ERROR");
($title,$pass,$home,$home_icon,$back_icon,$next_icon,$bg_img,$style_file,$bg_color,$title_color,$com_color,$com_adm,$catcols,$text_color,$regbg_color,@cat) = split(/<>/,<IN>);
close IN;
($sec,$min,$hour,$nowday,$nowmon,$nowyear) = localtime;
$nowyear += 1900;
$nowmon++;

if (!$logyear) {$logyear = $nowyear; $logmon = $nowmon;}
$logfile = "$base/d$logyear$logmon.txt";

if ($mode eq 'regin') {&regin;}
elsif ($mode eq 'search') {&search;}
elsif ($mode eq 'admin') {&admin;}
else {&main;}

print "</center></body></html>\n";
exit;

###
sub header {
	print "Content-type: text/html\n\n";
	print "<html><head><META HTTP-EQUIV=\"Content-type\" CONTENT=\"text/html; charset=Shift_JIS\">\n";
	print "<title>$title</title><link rel=\"stylesheet\" type=\"text/css\" href=\"$style_file\"></head>\n";
	$head = 1;
}

###
sub main {
	&header;
	print "<body background=\"$bg_img\" bgcolor=\"$bg_color\" text=\"$text_color\"><center>\n";
	print "<table width=98%><tr><td width=100 valign=top>";
	if ($home) {if ($home_icon) {print "<a href=\"$home\"><img src=\"$home_icon\" border=0></a>";} else {print "<a href=\"$home\">[HOME]</a>";}}
	print "</td><td align=center><font color=\"$title_color\" size=\"+1\"><b>$title</b></font></td><td width=100></td></tr></table>\n";
	if ($com_adm) {print "<table><tr><td><font color=\"$com_color\">$com_adm</font></td></tr></table>\n";}

	print "<table cellspacing=1 cellpadding=0>\n";
	$k = 0;
	for ($i=0; $i<$catmax; $i+=2) {
		$catcolor = $cat[$i+1];
		if (!$catcolor) {next;}
		if (!$k) {print "<tr>";}
		print "<td><font color=\"$catcolor\">��$cat[$i]</font></td><td width=20></td>\n";
		$k++;
		if ($k == $catcols) {print "</tr>"; $k = 0;}
	}
	if ($k) {print "</tr>";}
	print "</table>\n";
	&cal_dsp;
	print "<table width=96%><tr><td align=right><a href=\"$script?mode=admin\">[�Ǘ�]</a></td></tr></table>\n";
	# ���̍s�͒��쌠�\���ł��̂ō폜���Ȃ��ŉ������B#
	print "<a href=\"http://merlion.cool.ne.jp/cgi/\" target=\"_blank\">CGI-design</a>\n";
}

###
sub cal_dsp {
	if (-e $logfile) {
		open (IN,"$logfile") || &error("OPEN ERROR");
		while (<IN>) {
			($no,$day,$name,$com,$color,$pwd,$regaddr,$sub) = split(/<>/);
			$lognum[$day]++;
			$dn = "$day-$lognum[$day]";
			$logno{$dn} = $no;
			if ($sub) {$sub = "<b>$sub�@</b>";}
			$logcom{$dn} = "$sub$com�@<b>�y$name�z</b>";
			$logcolor{$dn} = $color;
		}
		close IN;
	}
	$mdays = $mdays[$logmon - 1];
	if ($logmon == 2 && $logyear % 4 == 0) {$mdays = 29;}

	print "<table width=95% cellspacing=8><tr><td width=120>\n";
	$year = $logyear - 1;
	$mon = 12;
	if (2002 < $year) {print "<a href=\"$script?mode=$mode&year=$year&mon=$mon\"><img src=\"$back_icon\" border=0></a>�@";}
	print "<font size=\"+1\"><b>$logyear�N</b></font>";
	$year = $logyear + 1;
	$mon = 1;
	print "�@<a href=\"$script?mode=$mode&year=$year&mon=$mon\"><img src=\"$next_icon\" border=0></a></td>\n";
	print "<td align=center><table bgcolor=\"#888888\" cellspacing=1 cellpadding=2><tr bgcolor=\"#f8f8f8\" align=center>\n";
	foreach (1 .. 12) {
		if ($_ == $logmon) {print "<td width=40 bgcolor=\"#ffff00\"><font color=\"#000000\"><b>$_��</b></font></td>\n";}
		else {print "<td width=40><a href=\"$script?mode=$mode&year=$logyear&mon=$_\">$_��</a></td>\n";}
	}
	print "</tr></table></td><td width=120 align=right>\n";
	if (!$mode) {print "<a href=\"$script?mode=regin&year=$logyear&mon=$logmon\">[�o�^]</a>�@<a href=\"$script?mode=search&year=$logyear\">[����]</a>";}
	print "</td></tr></table>\n";

	$def = 0.242194*($logyear-1980)-int(($logyear-1980)/4);
	$spr = int(20.8431+$def);
	$aut = int(23.2488+$def);
	%holi_d = ('0101','����','0211','�����L�O�̓�',"03$spr",'�t���̓�','0429','�݂ǂ�̓�','0503','���@�L�O��','0505','���ǂ��̓�',"09$aut",'�H���̓�','1103','�����̓�','1123','�ΘJ���ӂ̓�','1223','�V�c�a����');
	%holi_w = ('012','���l�̓�','073','�C�̓�','093','�h�V�̓�','102','�̈�̓�');

	print "<table width=97% bgcolor=\"#aaaaaa\" cellspacing=1 cellpadding=2><col span=2 align=center>\n";
	&get_date($logyear,$logmon,1);
	$w = $wday;
	$n = 0;
	for ($k=1; $k<=$mdays; $k++) {
		if ($w == 1) {$n++;}
		$wcolor = $wcolor[$w];
		if (!$w) {$bc = "#fef0ef";} elsif ($w == 6) {$bc = "#eeffff";} else {$bc = "#ffffff";}
		$holiday_dsp = '';
		&get_holiday($logmon,$k);
		if ($holiday) {
			$bc = "#fef0ef";
			$wcolor = $wcolor[0];
			$holiday_dsp = " <font color=\"$wcolor\" size=\"-1\">[$holiday]</font><br>";
		}
		if ($logyear == $nowyear && $logmon == $nowmon && $k == $nowday) {$bcday = ' bgcolor="#ffff00"';} else {$bcday = '';}

		print "<tr bgcolor=\"$bc\"><td width=30><font color=\"$wcolor\"><b>$k</b></font></td><td width=20><font color=\"$wcolor\">$week[$w]</font></td><td$bcday>$holiday_dsp\n";
		if ($lognum[$k]) {
			foreach (1 .. $lognum[$k]) {
				$dn = "$k-$_";
				$com = $logcom{$dn};
				$com =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\" target=\"_blank\">$2<\/a>/g;
				print "<table width=100% cellspacing=0 cellpadding=0><tr><td><font color=\"$logcolor{$dn}\">$com</font></td>\n";
				if ($mode eq 'regin') {print "<td width=40 valign=top><a href=\"$script?mode=regin&act=edt&year=$logyear&mon=$logmon&no=$logno{$dn}\">[�C��]</a></td>";}
				print "</tr></table>\n";
			}
		}
		print "</td></tr>\n";
		$w++;
		if (6 < $w) {$w = 0;}
	}
	print "</table>\n";
}

###
sub get_date {
	$y = $_[0];
	$m = $_[1];
	if( $m < 3 ){$y--; $m+=12;}
	$wday = ($y+int($y/4)-int($y/100)+int($y/400)+int((13*$m+8)/5)+$_[2])%7;
}

###
sub get_holiday {
	$sm = sprintf("%02d%02d",$_[0],$_[1]);
	$holiday = $holi_d{$sm};
	if ($sm eq '0504' && 1<$w) {$holiday = '�����̋x��';}
	if ($holiday && !$w) {$hflag = 1;}
	if (!$holiday && $w == 1) {
		$smw = sprintf("%02d$n",$_[0]);
		$holiday = $holi_w{$smw};
		if ($hflag) {$holiday = '�U�֋x��'; $hflag = 0;}
	}
}

###
sub regin {
	if ($wrt eq 'new') {&newwrt;}
	elsif ($wrt eq 'edt') {&edtwrt;}
	elsif ($wrt eq 'del') {&delwrt;}

	&header;
	print "<body background=\"$bg_img\" bgcolor=\"$bg_color\" text=\"$text_color\"><center>\n";
	print "<table width=97%><tr><td><a href=\"$script\">[Return]</a></td></tr></table>\n";
	if ($act) {&edtin; print "<b>***** �C���E�폜�@*****</b>\n";} else {print "<b>*****�@�V�K�o�^�@*****</b>\n";}
	&in_form;
	print "<br><hr width=97%>�C���E�폜����ꍇ�́u�C���v���N���b�N���ĉ������B<br>\n";
	&cal_dsp;
}

###
sub edtin {
	open (IN,"$logfile") || &error("OPEN ERROR");
	while (<IN>) {
		($no,$day,$name,$com,$color,$pwd,$regaddr,$sub) = split(/<>/);
		if ($in{'no'} eq $no) {last;}
	}
	close IN;

	if ($regaddr ne $ENV{'REMOTE_ADDR'}) {
		if ($in{'pwd'} eq '') {
			print "<br><br><br><br><h4>�C���L�[����͂��ĉ�����</h4>\n";
			print "<form action=\"$script\" method=POST>\n";
			print "<input type=hidden name=mode value=\"regin\">\n";
			print "<input type=hidden name=act value=\"edt\">\n";
			print "<input type=hidden name=year value=\"$logyear\">\n";
			print "<input type=hidden name=mon value=\"$logmon\">\n";
			print "<input type=hidden name=no value=\"$in{'no'}\">\n";
			print "<input type=password name=pwd size=10 maxlength=8>\n";
			print "<input type=submit value=\"����\"></form>\n";
			print "</center></body></html>\n";
			exit;
		}
		$mat = &decrypt($in{'pwd'},$pass);
		if (!$mat) {
			if ($pwd eq "") {&error("�Y���̓o�^�f�[�^�ɏC���L�[���ݒ肳��Ă��܂���");}
			$mat = &decrypt($in{'pwd'},$pwd);
			if (!$mat) {&error("�C���L�[���Ⴂ�܂�");}
		}
	}
}

###
sub in_pwchk {
	open (IN,"$logfile") || &error("OPEN ERROR");
	while (<IN>) {
		($no,$day,$name,$com,$color,$pwd,$regaddr,$sub) = split(/<>/);
		if ($in{'no'} eq $no) {last;}
	}
	close IN;
	if ($regaddr eq $ENV{'REMOTE_ADDR'}) {return;}

	if ($in{'edtpw'} eq '') {&error;}
	$mat = &decrypt($in{'edtpw'},$pass);
	if ($mat) {return;}

	if ($pwd eq '') {&error;}
	$mat = &decrypt($in{'edtpw'},$pwd);
	if (!$mat) {&error;}
}

###
sub in_form {
	print "<table bgcolor=\"$regbg_color\" cellspacing=10><tr><td><table cellspacing=1 cellpadding=0><col span=1 align=center>\n";
	print "<form action=\"$script\" method=POST>\n";
	print "<input type=hidden name=mode value=\"regin\">\n";
	print "<tr><td>�� �t</td><td>\n";
	if (!$act) {
		print "<input type=hidden name=wrt value=\"new\">\n";
		print "<select name=year>\n";
		foreach (2009 .. $nowyear+15) {
			if ($_ == $logyear) {$sel = ' selected';} else {$sel = '';}
			print "<option value=\"$_\"$sel>$_</option>\n";
		}
		print "</select>�N <select name=mon>\n";
		foreach (1 .. 12) {
			if ($_ == $logmon) {$sel = ' selected';} else {$sel = '';}
			print "<option value=\"$_\"$sel>$_</option>\n";
		}
		print "</select>�� <select name=day>\n";
		foreach (1 .. 31) {
			if ($_ == 1) {$sel = ' selected';} else {$sel = '';}
			print "<option value=\"$_\"$sel>$_</option>\n";
		}
		print "</select>��";
		&getcook;
		$sub=$com='';
		$submit = '������';
	} else {
		print "<input type=hidden name=year value=\"$logyear\">\n";
		print "<input type=hidden name=mon value=\"$logmon\">\n";
		print "<input type=hidden name=wrt value=\"edt\">\n";
		print "<input type=hidden name=no value=\"$in{'no'}\">\n";
		print "<input type=hidden name=edtpw value=\"$in{'pwd'}\">\n";
		$com =~ s/<br>/\r/g;
		$pwd = '';
		$submit = '�C������';
		print "<b>$logyear�N$logmon��$day��</b>";
	}
	print "</td></tr>\n";
	print "<tr><td>�� �O</td><td><input class=text type=text name=name size=40 value=\"$name\"></td></tr>\n";
	print "<tr><td>�\\ ��</td><td><input class=text type=text name=sub size=40 value=\"$sub\"></td></tr>\n";
	print "<tr><td valign=top><br>�� �e</td><td><textarea class=text cols=92 rows=6 name=com wrap=\"soft\">$com</textarea></td></tr>\n";
	print "<tr><td valign=top>�����F</td><td><table cellspacing=1 cellpadding=0>\n";
	if (!$color) {$color = $cat[1];}
	$k = 0;
	for ($i=0; $i<$catmax; $i+=2) {
		$catcolor = $cat[$i+1];
		if (!$catcolor) {next;}
		if (!$k) {print "<tr>";}
		if ($color eq $catcolor) {$chk = ' checked';} else {$chk = '';}
		print "<td width=30 bgcolor=\"$catcolor\" align=center><input type=radio name=color value=\"$catcolor\"$chk></td>\n";
		if ($cat[$i]) {print "<td><font color=\"$catcolor\">$cat[$i]</font></td><td width=20></td>\n";}
		$k++;
		if ($k == $catcols) {print "</tr>"; $k = 0;}
	}
	if ($k) {print "</tr>";}
	print "</table></td></tr>\n";
	print "<tr><td>�C���L�[</td><td><input class=text type=password name=pwd size=10 maxlength=8 value=\"$pwd\"> �i�p��8�����ȓ��j</td></tr>\n";
	print "<tr><td></td><td><table width=100% border=0 cellspacing=0 cellpadding=4><tr><td><input class=submit type=submit value=\"$submit\"></td></form>\n";
	if ($act) {
		print "<td width=40 bgcolor=red align=center>\n";
		print "<form action=\"$script\" method=POST>\n";
		print "<input type=hidden name=mode value=\"regin\">\n";
		print "<input type=hidden name=year value=\"$logyear\">\n";
		print "<input type=hidden name=mon value=\"$logmon\">\n";
		print "<input type=hidden name=wrt value=\"del\">\n";
		print "<input type=hidden name=no value=\"$in{'no'}\">\n";
		print "<input type=hidden name=edtpw value=\"$in{'pwd'}\">\n";
		print "<input type=submit value=\"�폜\"></td></form>\n";
	}
	print "</tr></table></td></tr></table></td></tr></table>\n";
}

###
sub newwrt {
	&in_chk;
	if ($in{'pwd'} ne '') {$pwd = &crypt($in{'pwd'});} else {$pwd = '';}

	&lock;
	open (IN, "$nofile") || &error("OPEN ERROR"); 		$no = <IN>; 		close IN;
	$no++;
	open (OUT, ">$nofile") || &error("OPEN ERROR");		print OUT $no;		close OUT;
	$newdata = "$no<>$in{'day'}<>$in{'name'}<>$in{'com'}<>$in{'color'}<>$pwd<>$ENV{'REMOTE_ADDR'}<>$in{'sub'}<>\n";

	if (-e $logfile) {
		$flag = 0;
		open (IN,"$logfile") || &error("OPEN ERROR");
		while (<IN>) {
			($no,$day) = split(/<>/);
			if ($in{'day'} < $day && !$flag) {push(@new,$newdata); $flag = 1;}
			push(@new,$_);
		}
		close IN;
		if (!$flag) {push(@new,$newdata);}
		open (OUT,">$logfile") || &error("OPEN ERROR");		print OUT @new;			close OUT;
	} else {
		open (OUT,">$logfile") || &error("OPEN ERROR");		print OUT $newdata;		close OUT;	chmod(0666,$logfile);
	}
	&unlock;
	&setcook;
}

###
sub in_chk {
	if (!$in{'name'}) {&error("���O����͂��ĉ������B");}
	if (!$in{'com'}) {&error("���e����͂��ĉ������B");}
	$in{'com'} =~ s/\r\n|\n|\r/<br>/g;
}

###
sub edtwrt {
	&in_pwchk;
	&in_chk;
	&lock;
	open (IN,"$logfile") || &error("OPEN ERROR");
	while (<IN>) {
		($no,$day,$name,$com,$color,$pwd,$regaddr) = split(/<>/);
		if ($in{'no'} eq $no) {
			if ($in{'pwd'} ne '') {$pwd = &crypt($in{'pwd'});}
			push(@new,"$no<>$day<>$in{'name'}<>$in{'com'}<>$in{'color'}<>$pwd<>$regaddr<>$in{'sub'}<>\n");
		} else {push(@new,$_);}
	}
	close IN;
	open (OUT,">$logfile") || &error("OPEN ERROR");		print OUT @new;		close OUT;
	&unlock;
}

###
sub delwrt {
	&in_pwchk;
	&lock;
	open (IN,"$logfile") || &error("OPEN ERROR");
	while (<IN>) {
		($no) = split(/<>/);
		if ($in{'no'} ne $no) {push(@new,$_);}
	}
	close IN;
	open (OUT,">$logfile") || &error("OPEN ERROR");		print OUT @new;		close OUT;
	&unlock;
}

###
sub search {
	&header;
	print "<body><center>\n";
	print "<table width=97%><tr><td><a href=\"$script\">[Return]</a></td></tr></table>\n";
	print "�L�[���[�h����͂��u�����v���N���b�N���ĉ������B�L�[���[�h�𕡐��w�肷��ꍇ�̓X�y�[�X�ŋ�؂��ĉ������B\n";
	print "<form action=\"$script\" method=POST>\n";
	print "<input type=hidden name=mode value=\"search\">\n";
	print "�L�[���[�h <input type=text name=word size=50 value=\"$in{'word'}\">\n";
	print "�@<select name=year>";
	foreach (2003 .. $nowyear+1) {
		if ($_ == $logyear) {$sel = ' selected';} else {$sel = '';}
		print "<option value=\"$_\"$sel>$_</option>\n";
	}
	print "</select>�N�@�@<input type=submit value=\" ���� \"></form>\n";
	if (!$in{'word'}) {print "</center></body></html>\n"; exit;}

	$in{'word'} =~ s/�@/ /g;
	@word = split(/\s+/,$in{'word'});
	$m = 0;
	foreach $mon (1 .. 12) {
		$logfile = "$base/d$logyear$mon.txt";
		if (!-e $logfile) {next;}
		@data = ();
		open (IN,"$logfile") || &error("OPEN ERROR");
		while (<IN>) {
			$find = 0;
			foreach $word (@word) {if (0 <= index($_,$word)) {$find = 1;} else {$find = 0; last;}}
			if ($find) {push(@data,$_); $m++;}
		}
		close IN;

		if (!$data[0]) {next;}
		print "<table width=95%><tr><td><b>$mon��</b></td></tr></table>\n";
		print "<table width=97% bgcolor=\"#aaaaaa\" cellspacing=1 cellpadding=2>\n";
		print "<tr bgcolor=\"#eeeeee\" align=center><td width=80>�� �t</td><td>���@�@�e</td><td width=100>�� �O</td></tr>\n";
		foreach (@data) {
			($no,$day,$name,$com,$color,$pwd,$regaddr,$sub) = split(/<>/);
			print "<tr bgcolor=\"#ffffff\"><td>�@","$logyear.$mon.$day</td><td><font color=\"$color\"><b>$sub</b>�@ $com</font></td><td>$name</td></tr>\n";
		}
		print "</table><br>\n";
	}
	print "�������ʁF �v <b>$m</b>��\n";
}

###
sub admin {
	&header;
	print "<body><center>\n";
	print "<table width=97%><tr><td><a href=\"$script\">[Return]</a></td></tr></table>\n";
	if ($in{'pass'} eq '') {
		print "<br><br><br><br><h4>�p�X���[�h����͂��ĉ�����</h4>\n";
		print "<form action=\"$script\" method=POST>\n";
		print "<input type=hidden name=mode value=\"admin\">\n";
		print "<input type=password name=pass size=10 maxlength=8>\n";
		print "<input type=submit value=\"�F��\"></form>\n";
		print "</center></body></html>\n";
		exit;
	}
	$mat = &decrypt($in{'pass'},$pass);
	if (!$mat) {&error("�p�X���[�h���Ⴂ�܂�");}

	if ($wrt) {
		if ($in{'newpass'} ne '') {$pass = &crypt($in{'newpass'});}
		$title = $in{'title'};
		$com_adm = $in{'com'};	$com_adm =~ s/\r\n|\r|\n/<br>/g;
		$home = $in{'home'};
		$home_icon = $in{'home_icon'};
		$back_icon = $in{'back_icon'};
		$next_icon = $in{'next_icon'};
		$bg_img = $in{'bg_img'};
		$style_file = $in{'style_file'};

		$bg_color = $in{'color0'};
		$text_color = $in{'color1'};
		$title_color = $in{'color2'};
		$com_color = $in{'color3'};
		$regbg_color = $in{'color4'};
		$catcols = $in{'catcols'};

		$opdata = "$title<>$pass<>$home<>$home_icon<>$back_icon<>$next_icon<>$bg_img<>$style_file<>$bg_color<>$title_color<>$com_color<>$com_adm<>$catcols<>$text_color<>$regbg_color";
		foreach (0 .. $catmax-1) {
			$cat[$_] = $in{"cat$_"};
			$opdata .= "<>$cat[$_]";
		}
		open (OUT, ">$opfile") || &error("OPEN ERROR");		print OUT $opdata;		close OUT;
	}
	print "���L�ɓ��͌�A�u�ݒ肷��v�������ĉ������B\n";
	print "<form action=\"$script\" method=POST>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=wrt value=\"on\">\n";
	print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
	print "<input type=submit value=\"�ݒ肷��\"><br><br>\n";

	print "<table bgcolor=\"#dddddd\" cellspacing=10><tr><td><table cellspacing=1 cellpadding=0>\n";
	print "<tr><td><b>�^�C�g��</b></td><td><input type=text name=title size=40 value=\"$title\"></td></tr>\n";
	$com_adm =~ s/<br>/\r/g;
	print "<tr><td valign=top><br><b>�R�����g</b></td><td><textarea cols=60 rows=6 name=com wrap=\"soft\">$com_adm</textarea></td></tr>\n";
	print "<tr><td><b>�z�[��URL</b></td><td><input type=text size=60 name=home value=\"$home\"></td></tr>\n";
	print "<tr><td><b>�z�[���A�C�R��</b></td><td><input type=text size=60 name=home_icon value=\"$home_icon\">";
	if ($home_icon) {print "�@<img src=\"$home_icon\">";}
	print "</td></tr>\n";
	print "<tr><td><b>BACK�A�C�R��</b></td><td><input type=text size=60 name=back_icon value=\"$back_icon\">�@<img src=\"$back_icon\"></td></tr>\n";
	print "<tr><td><b>NEXT�A�C�R��</b></td><td><input type=text size=60 name=next_icon value=\"$next_icon\">�@<img src=\"$next_icon\"></td></tr>\n";
	print "<tr><td><b>�ǎ�</b></td><td><input type=text size=60 name=bg_img value=\"$bg_img\">";
	if ($bg_img) {print "�@<img src=\"$bg_img\" width=30>";}
	print "</td></tr>\n";
	print "<tr><td><b>�X�^�C���V�[�g</b></td><td><input type=text size=60 name=style_file value=\"$style_file\"></td></tr>\n";

	print "<tr><td></td><td><a href=\"$base/color.htm\" target=\"_blank\">�J���[�R�[�h</a></td></tr>\n";
	@name = ('��{�w�i�F','��{�����F','�^�C�g���F','�R�����g�F','���͔w�i�F');
	@data = ($bg_color,$text_color,$title_color,$com_color,$regbg_color);
	foreach (0 .. $#name) {
		print "<tr><td><b>$name[$_]</b></td><td><table cellspacing=0 cellpadding=0><tr>\n";
		print "<td><input type=text name=color$_ size=10 value=\"$data[$_]\"></td>\n";
		print "<td width=5></td><td width=80 bgcolor=\"$data[$_]\"></td></tr></table></td></tr>\n";
	}
	print "<tr><td><b>�����F�\\��</b></td><td><input type=text size=4 name=catcols value=\"$catcols\">��</td></tr>\n";
	print "<tr><td valign=top><b>�����F����</b></td><td><table cellspacing=1 cellpadding=0>\n";
	for ($i=0; $i<$catmax; $i+=2) {
		print "<tr><td><input type=text name=cat$i size=24 value=\"$cat[$i]\">�@<input type=text name=cat",$i+1," size=10 value=\"$cat[$i+1]\"></td>\n";
		print "<td width=5></td><td width=30 bgcolor=\"$cat[$i+1]\"></td></tr>\n";
	}
	print "</table></td></tr>\n";
	print "<tr><td><b>�p�X���[�h�ύX</b></td><td><input type=password name=newpass size=10 maxlength=8> �i�p��8�����ȓ��j</td></tr>\n";
	print "</table></td></tr></table></form>\n";
}

###
sub setcook {
	my($sec,$min,$hour,$mday,$mon,$year,$wday) = gmtime(time+60*24*60*60);
	$ww = (Sun,Mon,Tue,Wed,Thu,Fri,Sat)[$wday];
	$month = (Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec)[$mon];
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",$ww,$mday,$month,$year+1900,$hour,$min,$sec);
	$cook = "$in{'name'}<>$in{'color'}<>$in{'pwd'}<>";
	print "Set-Cookie: sche27=$cook; expires=$gmt;\n";
}

###
sub getcook {
	if ($wrt eq 'new') {
		$name = $in{'name'};
		$color = $in{'color'};
		$pwd = $in{'pwd'};
		return;
	}
	my($n, $val, @pair);
	@pair = split(/;\s*/, $ENV{'HTTP_COOKIE'});
	foreach (@pair) {
		($n,$val) = split(/=/);
		$cook{$n} = $val;
	}
	($name,$color,$pwd) = split(/<>/, $cook{'sche27'});
}

###
sub lock {
	$retry = 3;
	if (-e $lockfile) {
		$locktime = (stat($lockfile))[9];
		if ($locktime < time - 60) {&unlock;}
	}
	while (!mkdir($lockfile,0755)) {
		if (--$retry < 0) {&error("busy!");}
		sleep(1);
	}
}

###
sub unlock {rmdir($lockfile);}

###
sub crypt {
	@salt = ('a' .. 'z','A' .. 'Z','0' .. '9');
	srand;
	$salt = "$salt[int(rand($#salt))]$salt[int(rand($#salt))]";
	return crypt($_[0],$salt);
}

###
sub decrypt {
	$salt = $_[1] =~ /^\$1\$(.*)\$/ && $1 || substr($_[1],0,2);
	if (crypt($_[0],$salt) eq $_[1] || crypt($_[0],'$1$' . $salt) eq $_[1]) {return 1;}
	return 0;
}

###
sub error {
	if (!$head) {&header; print "<body><center>\n";}
	print "<br><br><br><br><h3>ERROR !!</h3><font color=red><b>$_[0]</b></font>\n";
	print "</center></body></html>\n";
	exit;
}
