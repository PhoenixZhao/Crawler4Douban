
#normlization !!!
#越高越好，但是要在一定程度上避免 平均分比较低 但是 评分人数高的电影
#虽然有时候也需要这样
rating_total = (rating_av * ratings_c)/(10*ratings_c_max)

#可以反映一个电影的受欢迎程度
popularity = (do_c + collect_c + wish_c)/dcw_max

#trends如果太小，那么就说明这个电影已经过气了,而如果wish_c比较多，则说明最近比较火. 注意这个值在normalize之前可能会大于1
#最近的火热程度
trends = (wish_c/(collect_c+do_c))/tr_max if collect_c != 0 else 0

#观后感，反应影片的深刻程度
impressive = 0.3*comments_c/comments_c_max + 0.7*reviews_c/reviews_c_max

#temp adjustment
rating_total = f_tu(rating_total)
impressive = f_tu(impressive)


#it is a measure of whether a movie should be addBoost, =1 means it is a  totally good movie which should be boosted
boostProb = 0.6*f(rating_total) + 0.2*f(impressive) + 0.15*popularity + 0.05*trends

结果：
3412830:狄仁杰之通天帝国/2.5705194
5996801:狄仁杰之神都龙王/1.721988
4090554:少年狄仁杰/1.0000805
2995948:神探狄仁杰/1.0141044

分析：少年狄仁杰 和 神探狄仁杰 的权重过于接近，估计是因为 
rating_total = (rating_av * ratings_c)/(10*ratings_c_max)
分母太大，将数值变低了

解决：
直接使用 平均打分/10  或者在搜索之后进行一个数值拉伸



---

平均打分/10

#normlization !!!
#越高越好，但是要在一定程度上避免 平均分比较低 但是 评分人数高的电影
#虽然有时候也需要这样
rating_total = (rating_av * ratings_c)/(10*ratings_c_max)

#可以反映一个电影的受欢迎程度
popularity = (do_c + collect_c + wish_c)/dcw_max

#trends如果太小，那么就说明这个电影已经过气了,而如果wish_c比较多，则说明最近比较火. 注意这个值在normalize之前可能会大于1
#最近的火热程度
trends = (wish_c/(collect_c+do_c))/tr_max if collect_c != 0 else 0

#观后感，反应影片的深刻程度
impressive = 0.3*comments_c/comments_c_max + 0.7*reviews_c/reviews_c_max

#temp adjustment
rating_total = f_tu(rating_total)
impressive = f_tu(impressive)


#it is a measure of whether a movie should be addBoost, =1 means it is a  totally good movie which should be boosted
boostProb = 0.5*f(float(rating_av)/10) + 0.3*f(impressive) + 0.15*popularity + 0.05*trends

#print rating_total, impressive, popularity, trends
return boostProb

2995948:神探狄仁杰-->5.086066
4160349:狄仁杰断案传奇-->5.3493004
3412830:狄仁杰之通天帝国-->5.060738
4090554:少年狄仁杰-->3.7194934
5996801:狄仁杰之神都龙王-->5.009498
3190095:月上江南之狄仁杰洗冤录-->4.2933254
6808707:护国良相狄仁杰之风摧边关-->4.693164
3892394:仁医-->5.3154483

分析：显然平均分/10的数值相对较大，导致平均分权重太高，而人数的权重在数值上相对较低
解决：适当给予平均分/10降低数值，并增加人数权重

---

	#it is a measure of whether a movie should be addBoost, =1 means it is a  totally good movie which should be boosted
	boostProb = 0.4*f(float(rating_av)*0.5/10) + 0.4*f(impressive) + 0.15*popularity + 0.05*trends

2995948:神探狄仁杰-->2.305008
4160349:狄仁杰断案传奇-->2.5048697
3412830:狄仁杰之通天帝国-->2.9580033
5996801:狄仁杰之神都龙王-->2.659228
4090554:少年狄仁杰-->1.7106367
3190095:月上江南之狄仁杰洗冤录-->1.9175633
6808707:护国良相狄仁杰之风摧边关-->2.0888815
10801896:护国良相狄仁杰之古墓惊雷-->1.0000381

神探狄仁杰评分 8.1 
狄仁杰断案传奇是一个很老很小众的电视剧，但是评分居然有 8.6！！！
大部分评分都集中在 1-3 这个范围， f函数的作用有没有体现？ 如果没有作用，反而可能会起副作用


想到：用户搜索的关键词对应的可能 boost 都不是很高， 怎么能在这些结果中达到区分的效果：使用  数值拉伸 并且 使用修改的f 函数


---

	boostProb = 0.4*(float(rating_av)*0.5/10) + 0.4*impressive + 0.15*popularity + 0.05*trends


3412830:狄仁杰之通天帝国-->3.5397623
2995948:神探狄仁杰-->2.4961658
4160349:狄仁杰断案传奇-->2.6035857
4090554:少年狄仁杰-->2.0261774
5996801:狄仁杰之神都龙王-->3.2528517
3190095:月上江南之狄仁杰洗冤录-->2.1892247
6808707:护国良相狄仁杰之风摧边关-->2.3143885
10801896:护国良相狄仁杰之古墓惊雷-->1.0001074

加权的结果虽然是比较合理的，但是大家都进行了很大的加权，神都龙王的 3.25的加权意义就不大了

解决：

1. 数值上进行区分
2. 直接按照权值排序！



---

#人工排序
    retList = sorted(retList, key=operator.itemgetter('boost'), reverse=True)  

3412830:狄仁杰之通天帝国-->3.5397623
5996801:狄仁杰之神都龙王-->3.2528517
10561898:仁显王后的男人-->3.11168
4881202:仁医 完结篇-->2.7670016
3892394:仁医-->2.719505
2963313:百年拜仁-->2.6979835
3581476:太空堡垒卡拉狄加  第一季-->2.6315176
3581471:太空堡垒卡拉狄加  第二季-->2.6295528
3581466:太空堡垒卡拉狄加 第四季-->2.6153116
4225354:席琳·狄翁：全世界的目光-->2.6150103


不可行

想到：boostProb 需要保证有的doc能达到1 !!!!!!!!!!!!!!!!!!!!!!!!!
在 getMax的时候就进行各个因子的加权，得到一个 tmp_prob，（每个因子需要 数值归一化 权重需要考虑 但是权重之和不必再为1,但是数值也必须在一个量级）
这样就可以进行将prob进行归一，


---

	boostProb = 0.4*(float(rating_av)*0.3/10) + 0.4*impressive + 0.15*popularity + 0.05*trends


3412830:狄仁杰之通天帝国-->3.0789623
5996801:狄仁杰之神都龙王-->2.7560518
4160349:狄仁杰断案传奇-->1.9627856
2995948:神探狄仁杰-->1.9129657
4090554:少年狄仁杰-->1.6157774
3190095:月上江南之狄仁杰洗冤录-->1.7140247
6808707:护国良相狄仁杰之风摧边关-->1.7887884
10801896:护国良相狄仁杰之古墓惊雷-->1.0001074

结果还是可以的



#为了减少一个电影由于太过热门，而把一些不够热门的好电影给去掉，电影热门程度在权重和评分中的比重应该是一个 sqrt类型的凸函数，甚至
可以是一个 /— 型的函数






@7. Wrapper：


@1. tags 长度？ norm？ 这样就不用在开始对比较热门的电影增加过多的权值 

4. 分词

@5. 统计 ML:sklearn

6. 时间信息 作为因子 已经将时间格式统一

2. 提前加权，是为了把好电影，热门电影能够排在前1000？ 加权力度要控制好

3. 得到lucene的score，进行事后加权

		问题：如何将 tag:人性 中的 人数体现出来

		Index的时候加权：
		不能整体加权，不能区分

		查询到来时：
		计算相关度的时候加权，过来一个query，在search tags 域的时候考虑人数信息：
		How？

		1. 评论人数 在实际情况中相当于 tf 即 词频， 可以修改打分公式中的 tf，将其由 1或者0（现有情况下的tag）替换为 评分人数
		但是要修改评分公式，可能会造成系统不稳定.
		
		2. 直接填充，这太傻比了, 而且内存不足
		测试之后发现：有的电影评论人数太多，1w+ 那么给定一个区间 500 ，让这 1w+/500 ，相当于线性的变换到一个小区间，

		3. 接到用户query之后，进行Index，重新调整权值。。。不管怎么说，这是一个思路

		我还是觉得1是最靠谱的方法！但是好难，使用2

		查询结束后：
		加权，排序


* 填充 tags(已填充'￥￥￥<>0') ， 得到score ， 验证wrapper  == ok

* tf ok

* 加权（增加时间因子、tags人数因子，） 调参数


#span 500
1978709:黑天鹅boost->4.884996|| score:8.27116107941
2334904:禁闭岛boost->4.1246505|| score:8.27116107941
3541415:盗梦空间boost->6.8182135|| score:8.27116107941
3836070:孤独的生还者boost->4.0984836|| score:8.27116107941
5323968:环太平洋boost->4.0733876|| score:8.27116107941
1783457:功夫熊猫boost->3.854173|| score:7.23726606369
1858711:玩具总动员3boost->3.5222535|| score:7.23726606369
1905462:荒野生存boost->3.7335868|| score:7.23726606369
2336785:爱丽丝梦游仙境boost->3.8150325|| score:7.23726606369
1298624:闻香识女人boost->3.9140494|| score:7.23726606369
4206436:战马boost->3.7987738|| score:7.23726606369

效果有一些改善 目测电影热门程度占的权重还是比较多
功夫熊猫？？？？？？

*目测是因为没有在填充的tags之间加入空格！！！*

2334904:禁闭岛boost->4.1246505|| score:8.27116107941
3541415:盗梦空间boost->6.8182135|| score:8.27116107941
3836070:孤独的生还者boost->4.0984836|| score:8.27116107941
1978709:黑天鹅boost->4.884996|| score:8.27116107941
5323968:环太平洋boost->4.0733876|| score:8.27116107941
2336785:爱丽丝梦游仙境boost->3.8150325|| score:7.23726606369
1298624:闻香识女人boost->3.9140494|| score:7.23726606369
4206436:战马boost->3.7987738|| score:7.23726606369
3592853:饥饿游戏boost->3.5571682|| score:7.23726606369
1783457:功夫熊猫boost->3.854173|| score:7.23726606369

???

#原来是命令输入错误 参数含有空格 需要加“”
5322596:超脱boost->3.4058418|| score:10.6782369614
1945330:迷雾boost->3.1574037|| score:9.6557302475
3592853:饥饿游戏boost->3.5571682|| score:9.64997005463
1298624:闻香识女人boost->3.9140494|| score:9.64489650726
4206436:战马boost->3.7987738|| score:9.48587226868
3075287:源代码boost->4.9240813|| score:8.81768417358
1300374:绿里奇迹boost->2.6136603|| score:8.09265327454
2969282:七磅boost->2.8750484|| score:7.5892739296

#比较热门的电影填充之后会起到稀释的作用（tags多，人数多） 可以在时候定一个标准长度(其实应该是一个最大长度！)
从 十二怒汉 来看 应该有100+
从 Inception 来看 6000+

span为500
LEN设置为 100 好了

5322596:超脱boost->3.4058418|| score:10.6782369614
1945330:迷雾boost->3.1574037|| score:9.6557302475
3592853:饥饿游戏boost->3.5571682|| score:9.64997005463
1298624:闻香识女人boost->3.9140494|| score:9.64489650726
4206436:战马boost->3.7987738|| score:9.48587226868
3075287:源代码boost->4.9240813|| score:8.81768417358
1300374:绿里奇迹boost->2.6136603|| score:8.09265327454
2969282:七磅boost->2.8750484|| score:7.5892739296
.
.
.
10583098:十二怒汉boost->1.9252125|| score:2.25972104073  (第50名)

5322596:超脱boost->3.4058418|| score:10.6782369614
1945330:迷雾boost->3.1574037|| score:9.6557302475
3592853:饥饿游戏boost->3.5571682|| score:9.64997005463
1298624:闻香识女人boost->3.9140494|| score:9.64489650726
4206436:战马boost->3.7987738|| score:9.48587226868
3075287:源代码boost->4.9240813|| score:8.81768417358
1300374:绿里奇迹boost->2.6136603|| score:8.09265327454
2969282:七磅boost->2.8750484|| score:7.5892739296
3364223:了不起的盖茨比boost->4.1151795|| score:6.95277881622
3649049:金陵十三钗boost->5.968081|| score:6.02896356583
2275370:战略特勤组boost->2.4965737|| score:5.96665859222

金陵十三钗是怎么回事？


python SearchMysql_v3.py "countries:美 国^5 user_tags:人性"
3592853:饥饿游戏boost->3.5571682|| score:10.3008670807
1298624:闻香识女人boost->3.9140494|| score:10.2980251312
4206436:战马boost->3.7987738|| score:10.2089385986
5322596:超脱boost->3.4058418|| score:10.1776332855
1945330:迷雾boost->3.1574037|| score:9.60482120514
3075287:源代码boost->4.9240813|| score:9.13534355164
1300374:绿里奇迹boost->2.6136603|| score:8.02990531921
2969282:七磅boost->2.8750484|| score:7.74791002274
3364223:了不起的盖茨比boost->4.1151795|| score:7.39134311676
2275370:战略特勤组boost->2.4965737|| score:6.13964080811
3895511:遗落战境boost->2.5639288|| score:6.11456775665

终于把金陵十三钗剔除了，但是饥饿游戏是什么玩意

开始的权值给的太大了，人数占的优势太多



#核心






1. 人为建立情感词库

2. tf-idf，本质上是将所有可能的词作为词库


可以吧 query在comments中的搜索评分也作为reRank的一个因子




#电影缺失问题
补充之后要更新maxDict


#可以算一下每个因子的分布区间，根据区间来调整系数


IndexReader:

	Terms 	getTermVector(int docID, String field)
	Retrieve term vector for this document and field, or null if term vectors were not indexed.

terms

	abstract TermsEnum 	iterator(TermsEnum reuse)
	Returns an iterator that will step through all terms.

TermsEnum

	docFreq()
	Returns the number of documents containing the current term.

	DocsEnum 	docs(Bits liveDocs, DocsEnum reuse)
	Get DocsEnum for the current term.

<!-- abstract BytesRef 	term()
Returns current term. -->

DocsEnum:

	abstract int 	freq()
	Returns term frequency in the current document.


MultiFields:

	static DocsEnum 	getTermDocsEnum(IndexReader r, Bits liveDocs, String field, BytesRef term)
	Returns DocsEnum for the specified field & term.

TermsEnum.docFreq():所有包含当前term的doc数目
TermsEnum。totalTermFreq： 该term再所有doc中的数目


	for (int i = 0; i < Reader.maxDoc(); ++i) {
	  Terms terms = Reader.getTermVector(i, "body");

		TermsEnum termsEnum = terms.iterator(null);
		int count = 0;
	    while (termsEnum.next() != null) {
			Term t = termsEnum.term();
			docFreq = TermsEnum.Freq()
				TermsEnum.docs(Bits liveDocs, DocsEnum reuse)
				reader, MultiFields.getLiveDocs(reader), "contents", term.bytes()

	        count++;
	    }
	}

IndexReader indexReader = DirectoryReader.open(directory);

Bits liveDocs = MultiFields.getLiveDocs(indexReader);
Fields fields = MultiFields.getFields(indexReader);
for (String field : fields) {

    TermsEnum termEnum = MultiFields.getTerms(indexReader, field).iterator(null);
    BytesRef bytesRef;
    while ((bytesRef = termEnum.next()) != null) {
        if (termEnum.seekExact(bytesRef, true)) {

            DocsEnum docsEnum = termEnum.docs(liveDocs, null);

            if (docsEnum != null) {
                int doc;
                while ((doc = docsEnum.nextDoc()) != DocIdSetIterator.NO_MORE_DOCS) {
                    System.out.println(bytesRef.utf8ToString() + " in doc " + doc + ": " + docsEnum.freq());
                }
            }
        }
    }
}

for (String field : fields) {
    TermsEnum termEnum = MultiFields.getTerms(indexReader, field).iterator(null);
    BytesRef bytesRef;
    while ((bytesRef = termEnum.next()) != null) {
        int freq = indexReader.docFreq(new Term(field, bytesRef));

        System.out.println(bytesRef.utf8ToString() + " in " + freq + " documents");

    }
}

呈献 in doc 23352: 1
呈献 in doc 44802: 1
呈献 in doc 54447: 1
呈献 in doc 153348: 1
呈献 in doc 157660: 1
呈献 in 5 documents

idf(t)  =   	1 + log ( 	
numDocs
–––––––––
docFreq+1
	)

在 23352 中：
tf = 1
idf = 5


特征矩阵
id   term1  term2   term3   
1
2
3

每个doc来一个 dict，或者list，其实list貌似更好，因为省时间，而且扫描的顺序都是一定的

	list = [docList1, docList2,...]

实际扫描因为是先扫term，所以是以列为主序，扫到一个term，然后看哪个文档有，塞到对应的docList ，以及对应的位置(当前term位置)


