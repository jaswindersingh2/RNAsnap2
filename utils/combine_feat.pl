#!/usr/bin/perl -w
use strict;

my $dir=$ARGV[0];
my $id=$ARGV[1];

	my @seq=`cat $dir/$id.fasta`;chomp(@seq);
	my @seq1=split(//,$seq[1]);chomp(@seq1);
	my @pssm=`cat $dir/$id.pssm`;chomp(@pssm);
	my $stru=`cat $dir/$id.stru`;chomp($stru);

	my @one_hot=&get_onehot($seq[1],$stru,@pssm);
	open(OUT,">$dir/$id.profile");
	for(my $i=0;$i<@pssm;$i++)
	{
			print OUT "1\t";
			for(my $j=0;$j<9;$j++)
			{
            	printf OUT ("%.6f\t",$one_hot[$i][$j]);
            }
			print OUT "\n";
        }


sub get_onehot{

	my ($seq,$stru,@pssm)=@_;
	my @seq=split(//,$seq);
	my @ss=split(/\t/,$stru);
	my @one_hot=();
	for(my $i=0;$i<@pssm;$i++)
	{
		for(my $j=0;$j<9;$j++)
		{
			$one_hot[$i][$j]=0;
		}
	}
    for(my $i=0;$i<@seq;$i++)
    {
		$one_hot[$i][0]=1 if($seq[$i] eq 'A');
        $one_hot[$i][1]=1 if($seq[$i] eq 'U' || $seq[$i] eq 'T');
        $one_hot[$i][2]=1 if($seq[$i] eq 'G');
		$one_hot[$i][3]=1 if($seq[$i] eq 'C');
		$one_hot[$i][8]=$ss[$i];
#		if($ss[$i] eq '.')
#		{
#			$one_hot[$i][8]=1;
#		}
#		else{
#			$one_hot[$i][8]=0;
#		}

		my @col=split(/\s+/,$pssm[$i]);
        my $sum=0;
		if($col[0] eq "A")
		{
			$col[1]+=8.7;
		}
		if($col[0] eq "U"|| $col[0] eq "T")
		{
			$col[2]+=8.7;
		}
		if($col[0] eq "G")
		{
			$col[3]+=8.7;
		}
		if($col[0] eq "C")
		{
			$col[4]+=8.7;
		}

        for(my $j=1;$j<@col-1;$j++)
        {
			$col[$j]+=0.3;
            $sum+=$col[$j];
        }
		$col[4]=log(4*$col[4]/($sum>1.0?$sum:1.0)/0.23); #C
		$col[3]=log(4*$col[3]/($sum>1.0?$sum:1.0)/0.23); #G
		$col[2]=log(4*$col[2]/($sum>1.0?$sum:1.0)/0.27); #U
		$col[1]=log(4*$col[1]/($sum>1.0?$sum:1.0)/0.28); #A

                for(my $j=1;$j<@col-1;$j++)
                {
                	$col[$j]=($col[$j] + 9.545)*2/(2.855 + 9.545)-1;#tr89 #ts44 #cn48 (2.855955,-9.545827) infernal and blast with fj
					$one_hot[$i][$j+3]=$col[$j];
                }
        }
	return @one_hot;
}
