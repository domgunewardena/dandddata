revenue_query = 'SELECT\
                T1."SiteCode",\
                T1."SiteName",\
                T1."Quarter",\
                T1."Period",\
                T1."LocationCode",\
                IFNULL("@REV_CC"."U_Name", CC."PrcName") AS "LocationName",\
                T1."GenericLocation",\
                T1."Session",\
                T1."OrdSession",\
                T1."RevenueType",\
                T1."Category",\
                T1."Wine",\
                T1."Year",\
                T1."FY",\
                T1."Month",\
                T1."OrdMonth",\
                T1."Week",\
                T1."Date",\
                T1."Day",\
                T1."OrdDay",\
                T1."Revenue"\
                FROM\
               (SELECT\
                OPRC."PrcCode" AS "SiteCode",\
                OPRC."PrcName" AS "SiteName",\
                "@CALENDAR"."U_Quarter" AS "Quarter",\
                OFPR."Name" AS "Period",\
                JDT1."OcrCode2" AS "LocationCode",\
                CASE WHEN JDT1."ProfitCode" = \'36\' AND JDT1."OcrCode2" = \'203\' THEN \'Bar\'\
                    ELSE CASE WHEN JDT1."OcrCode2" < \'205\' THEN \'Restaurant\'\
                    ELSE CASE WHEN JDT1."OcrCode2" BETWEEN \'205\' AND \'209\' THEN \'Events & Ex Hires\'\
                    ELSE CASE WHEN JDT1."OcrCode2" BETWEEN \'210\' AND \'219\' THEN \'Bar\'\
                    ELSE CASE WHEN JDT1."OcrCode2" BETWEEN \'220\' AND \'224\' THEN \'PDR\'\
                    ELSE \'Retail & Other\'\
                END END END END END AS "GenericLocation",\
                OACT."U_SessionTitle" AS "Session",\
                CASE OACT."U_SessionTitle"\
                WHEN \'Breakfast\' THEN \'1\'\
                WHEN \'Lunch\' THEN \'2\'\
                WHEN \'Dinner\' THEN \'3\'\
                WHEN \'Other\' THEN \'4\'\
                ELSE \'5\' END AS "OrdSession",\
                CASE LEFT(OACT."AcctCode", 3)\
                WHEN \'400\' THEN \'Food\'\
                WHEN \'401\' THEN \'Beverage\'\
                WHEN \'402\' THEN \'Tobacco\'\
                WHEN \'403\' THEN \'Room Sales\'\
                WHEN \'404\' THEN \'Other Revenue\'\
                WHEN \'406\' THEN \'Discounts\'\
                END AS "RevenueType",\
                "@SALES_MIX_CAT"."U_Category" AS "Category",\
                CASE WHEN UCASE("@SALES_MIX_CAT"."U_Category") LIKE \'%WINE%\' THEN \'Wine\'\
                ELSE \'Non-Wine\'\
                END AS "Wine",\
                "@CALENDAR"."U_Year" AS "Year",\
                "@CALENDAR"."U_FY" AS "FY",\
                "@CALENDAR"."U_Month" AS "Month",\
                "@CALENDAR"."U_OrdMonth" AS "OrdMonth",\
                "@CALENDAR"."U_WeekNo" AS "Week",\
                JDT1."RefDate" AS "Date",\
                "@CALENDAR"."U_Day" AS "Day",\
                "@CALENDAR"."U_OrdDay" AS "OrdDay",\
                SUM(JDT1."Credit" - JDT1."Debit") AS "Revenue"\
                FROM\
                "LIVE_DD_UK".JDT1 INNER JOIN "LIVE_DD_UK".OACT ON JDT1."Account" = OACT."AcctCode"\
                INNER JOIN "LIVE_DD_UK".OFPR ON JDT1."FinncPriod" = OFPR."AbsEntry"\
                INNER JOIN "LIVE_DD_UK".OPRC ON JDT1."ProfitCode" = OPRC."PrcCode"\
                INNER JOIN "DTW_DD_UK"."@CALENDAR" ON JDT1."RefDate" = "@CALENDAR"."U_Date"\
                LEFT OUTER JOIN "DTW_DD_UK"."@SALES_MIX_CAT" ON JDT1."U_Description2" = "@SALES_MIX_CAT"."U_Class"\
                           AND JDT1."ProfitCode" = "@SALES_MIX_CAT"."U_SiteCode"\
                WHERE\
                    OFPR."Name" >= \'19/20-01\'\
                    AND JDT1."Account" LIKE \'4%\'\
                    AND JDT1."ProfitCode" < \'60\'\
                GROUP BY\
                    OPRC."PrcCode",\
                    OPRC."PrcName",\
                    OPRC."U_CompSet3",\
                    "@CALENDAR"."U_Quarter",\
                    "@CALENDAR"."U_OrdMonth",\
                    OFPR."Name",\
                    LEFT(OFPR."Name", 5),\
                    OFPR."T_RefDate",\
                    JDT1."OcrCode2",\
                    JDT1."ProfitCode",\
                    OACT."U_SessionTitle",\
                    OACT."AcctCode",\
                    "@CALENDAR"."U_Year",\
                    "@CALENDAR"."U_FY",\
                    "@CALENDAR"."U_Month",\
                    "@CALENDAR"."U_WeekNo",\
                    "@CALENDAR"."U_OrdDay",\
                    JDT1."RefDate",\
                    "@CALENDAR"."U_Day",\
                    "@SALES_MIX_CAT"."U_Category") AS T1\
                LEFT OUTER JOIN "LIVE_DD_UK".OPRC CC ON T1."LocationCode" = CC."PrcCode"\
                LEFT OUTER JOIN "DTW_DD_UK"."@REV_CC" ON T1."SiteCode" = "@REV_CC"."U_SiteCode"\
                    AND T1."LocationCode" = "@REV_CC"."U_CostCentreCode"\
                ORDER BY\
                    T1."Date",\
                    T1."SiteCode",\
                    T1."LocationCode"'

covers_query = 'SELECT\
                T1."SiteCode",\
                T1."SiteName",\
                T1."VenueType",\
                T1."OrdType",\
                T1."Quarter",\
                T1."Period",\
                T1."PeriodEnd",\
                T1."LocationCode",\
                IFNULL("@REV_CC"."U_Name", CC."PrcName") AS "LocationName",\
                T1."GenericLocation",\
                T1."Session",\
                T1."Year",\
                T1."FY", \
                T1."Month",\
                T1."OrdMonth",\
                T1."Week",\
                T1."Date",\
                T1."Day",\
                T1."OrdDay",\
                T1."Covers"\
            FROM\
                (SELECT\
                    OPRC."PrcCode" AS "SiteCode",\
                    OPRC."PrcName" AS "SiteName",\
                    OPRC."U_CompSet3" AS "VenueType",\
                    CASE OPRC."U_CompSet3"\
                        WHEN \'UK Established\' THEN \'1\'\
                        WHEN \'UK Refurbished\' THEN \'2\'\
                        WHEN \'New Venture\' THEN \'3\'\
                    ELSE \'4\' END AS "OrdType",\
                    "@CALENDAR"."U_Quarter" AS "Quarter",\
                    OFPR."Name" AS "Period",\
                    OFPR."T_RefDate" AS "PeriodEnd",\
                    JDT1."OcrCode2" AS "LocationCode",\
                    CASE WHEN JDT1."ProfitCode" = \'36\' AND JDT1."OcrCode2" = \'203\' THEN \'Bar\'\
                        ELSE CASE WHEN JDT1."OcrCode2" < \'205\' THEN \'Restaurant\'\
                        ELSE CASE WHEN JDT1."OcrCode2" BETWEEN \'205\' AND \'209\' THEN \'Events & Ex Hires\'\
                        ELSE CASE WHEN JDT1."OcrCode2" BETWEEN \'210\' AND \'219\' THEN \'Bar\'\
                        ELSE CASE WHEN JDT1."OcrCode2" BETWEEN \'220\' AND \'224\' THEN \'PDR\'\
                        ELSE \'Retail & Other\'\
                    END END END END END AS "GenericLocation",\
                            JDT1."Account" AS "Account",\
                    CASE WHEN JDT1."Account" = 410010 THEN \'Breakfast\'\
                                 WHEN JDT1."Account" = 410020 THEN \'Lunch\'\
                                 WHEN JDT1."Account" = 410030 THEN \'Dinner\'\
                                 WHEN JDT1."Account" = 410040 THEN \'Night\'\
                    ELSE \'Other\' END AS "Session",\
                    "@CALENDAR"."U_Year" AS "Year",\
                    "@CALENDAR"."U_FY" AS "FY",\
                    "@CALENDAR"."U_Month" AS "Month",\
                    "@CALENDAR"."U_OrdMonth" AS "OrdMonth",\
                    "@CALENDAR"."U_WeekNo" AS "Week",\
                    JDT1."RefDate" AS "Date",\
                    "@CALENDAR"."U_Day" AS "Day",\
                    "@CALENDAR"."U_OrdDay" AS "OrdDay",\
                    SUM(JDT1."Debit") AS "Covers"\
                FROM\
                    "DTW_DD_UK".JDT1 INNER JOIN "DTW_DD_UK".OACT ON JDT1."Account" = OACT."AcctCode"\
                    INNER JOIN "DTW_DD_UK".OFPR ON JDT1."FinncPriod" = OFPR."AbsEntry"\
                    INNER JOIN "LIVE_DD_UK".OPRC ON JDT1."ProfitCode" = OPRC."PrcCode"\
                    INNER JOIN "DTW_DD_UK"."@CALENDAR" ON JDT1."RefDate" = "@CALENDAR"."U_Date"\
                WHERE\
                    OFPR."Name" >= \'19/20-01\'\
                    AND JDT1."Account" LIKE \'41%\'\
                    AND JDT1."ProfitCode" < \'60\'\
                GROUP BY\
                    OPRC."PrcCode",\
                    OPRC."PrcName",\
                    OPRC."U_CompSet3",\
                    "@CALENDAR"."U_Quarter",\
                    "@CALENDAR"."U_OrdMonth",\
                    OFPR."Name",\
                    OFPR."T_RefDate",\
                    JDT1."OcrCode2",\
                    JDT1."ProfitCode",\
                    JDT1."Account",\
                    "@CALENDAR"."U_Year",\
                    "@CALENDAR"."U_FY",\
                    "@CALENDAR"."U_Month",\
                    "@CALENDAR"."U_WeekNo",\
                    "@CALENDAR"."U_OrdDay",\
                    JDT1."RefDate",\
                    "@CALENDAR"."U_Day") AS T1\
                LEFT OUTER JOIN "DTW_DD_UK".OPRC CC ON T1."LocationCode" = CC."PrcCode"\
                LEFT OUTER JOIN "DTW_DD_UK"."@REV_CC" ON T1."SiteCode" = "@REV_CC"."U_SiteCode"\
                    AND T1."LocationCode" = "@REV_CC"."U_CostCentreCode"\
                ORDER BY\
                T1."Date",\
                T1."SiteCode",\
                T1."LocationCode"'

rev_df_columns = ['SiteName', 'LocationName', 'GenericLocation', 'Session', 'OrdSession', 'RevenueType', 'Wine', 'Date', 'Day', 'OrdDay', 'Revenue']
cov_df_columns = ['SiteName', 'LocationName', 'GenericLocation', 'Session', 'Date', 'Day', 'OrdDay', 'Covers']
